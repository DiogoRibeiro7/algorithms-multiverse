"""
Comprehensive Trie Data Structure Implementations in Python

This module implements multiple trie variants and applications:
1. Standard Trie
2. Compressed Trie (Patricia Tree)
3. Suffix Trie
4. Applications: Spell checker, Auto-complete, Dictionary

Time Complexity:
- Insert: O(m) where m is key length
- Search: O(m)
- Delete: O(m)
- Prefix Search: O(p + n) where p is prefix length, n is results
- Space: O(ALPHABET_SIZE * N * M) where N is number of keys

Advantages over Hash Tables:
✓ Prefix-based operations
✓ Ordered traversal
✓ No hash collisions
✓ Memory efficient for common prefixes

Use Cases:
- Auto-complete systems
- Spell checkers
- IP routing (longest prefix match)
- Dictionary implementations
- DNA sequence analysis
- Text prediction
"""

from typing import Dict, List, Optional, Tuple, Set
import json
from collections import defaultdict, deque

# ============================================================================
# STANDARD TRIE
# ============================================================================

class TrieNode:
    """Node in a standard trie."""

    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.frequency: int = 0  # For ranking suggestions

class Trie:
    """
    Standard Trie implementation.

    Features:
    - Insert, search, delete operations
    - Prefix search
    - Auto-completion
    - Word frequency tracking
    """

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word: str, frequency: int = 1) -> None:
        """Insert a word into the trie. O(m)"""
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end_of_word:
            self.word_count += 1

        node.is_end_of_word = True
        node.frequency = frequency

    def search(self, word: str) -> bool:
        """Search for exact word. O(m)"""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix. O(p)"""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Helper to find node for given prefix."""
        node = self.root

        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]

        return node

    def delete(self, word: str) -> bool:
        """Delete a word from trie. O(m)"""

        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            if index == len(word):
                if not node.is_end_of_word:
                    return False

                node.is_end_of_word = False
                self.word_count -= 1
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False

            child = node.children[char]
            should_delete_child = _delete_helper(child, word, index + 1)

            if should_delete_child:
                del node.children[char]
                return not node.is_end_of_word and len(node.children) == 0

            return False

        return _delete_helper(self.root, word, 0)

    def autocomplete(self, prefix: str, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get word suggestions for prefix.
        Returns list of (word, frequency) tuples.
        """
        node = self._find_node(prefix)
        if not node:
            return []

        suggestions = []

        def dfs(node: TrieNode, current_word: str):
            if node.is_end_of_word:
                suggestions.append((current_word, node.frequency))

            for char, child in sorted(node.children.items()):
                dfs(child, current_word + char)

        dfs(node, prefix)

        # Sort by frequency and limit results
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        return suggestions[:limit]

    def longest_common_prefix(self) -> str:
        """Find longest common prefix of all words."""
        if not self.root.children:
            return ""

        prefix = []
        node = self.root

        while len(node.children) == 1 and not node.is_end_of_word:
            char, child = next(iter(node.children.items()))
            prefix.append(char)
            node = child

        return ''.join(prefix)

    def get_all_words(self) -> List[str]:
        """Get all words in trie."""
        words = []

        def dfs(node: TrieNode, current: str):
            if node.is_end_of_word:
                words.append(current)
            for char, child in node.children.items():
                dfs(child, current + char)

        dfs(self.root, "")
        return sorted(words)

    def count_words_with_prefix(self, prefix: str) -> int:
        """Count how many words have given prefix."""
        node = self._find_node(prefix)
        if not node:
            return 0

        count = 0

        def dfs(node: TrieNode):
            nonlocal count
            if node.is_end_of_word:
                count += 1
            for child in node.children.values():
                dfs(child)

        dfs(node)
        return count

    def serialize(self) -> str:
        """Serialize trie to JSON string."""

        def node_to_dict(node: TrieNode) -> dict:
            return {
                'is_end': node.is_end_of_word,
                'freq': node.frequency,
                'children': {char: node_to_dict(child)
                           for char, child in node.children.items()}
            }

        return json.dumps(node_to_dict(self.root))

    @staticmethod
    def deserialize(data: str) -> 'Trie':
        """Deserialize trie from JSON string."""
        trie = Trie()

        def dict_to_node(d: dict) -> TrieNode:
            node = TrieNode()
            node.is_end_of_word = d['is_end']
            node.frequency = d['freq']
            for char, child_dict in d['children'].items():
                node.children[char] = dict_to_node(child_dict)
            return node

        root_dict = json.loads(data)
        trie.root = dict_to_node(root_dict)

        # Recount words
        def count_words(node: TrieNode) -> int:
            count = 1 if node.is_end_of_word else 0
            for child in node.children.values():
                count += count_words(child)
            return count

        trie.word_count = count_words(trie.root)
        return trie

# ============================================================================
# COMPRESSED TRIE (PATRICIA TREE)
# ============================================================================

class PatriciaNode:
    """Node in Patricia trie (compressed trie)."""

    def __init__(self, key: str = ""):
        self.key = key  # Edge label (can be multiple characters)
        self.children: Dict[str, 'PatriciaNode'] = {}
        self.is_end_of_word = False
        self.value: Optional[str] = None

class PatriciaTrie:
    """
    Compressed Trie (Patricia Tree).

    More space-efficient than standard trie by compressing
    chains of single-child nodes into single edges.

    Used in:
    - IP routing tables (CIDR)
    - Radix trees
    - Suffix trees
    """

    def __init__(self):
        self.root = PatriciaNode()

    def insert(self, word: str, value: str = None) -> None:
        """Insert word into Patricia trie."""
        if not word:
            return

        node = self.root
        remaining = word

        while remaining:
            # Find matching child
            matched_char = remaining[0]
            if matched_char not in node.children:
                # No matching child, create new node
                new_node = PatriciaNode(remaining)
                new_node.is_end_of_word = True
                new_node.value = value or word
                node.children[matched_char] = new_node
                return

            child = node.children[matched_char]

            # Find common prefix between remaining and child.key
            i = 0
            while (i < len(remaining) and i < len(child.key) and
                   remaining[i] == child.key[i]):
                i += 1

            if i == len(child.key):
                # Child key is prefix of remaining
                node = child
                remaining = remaining[i:]
            else:
                # Need to split the edge
                common = child.key[:i]

                # Create new intermediate node
                new_node = PatriciaNode(common)

                # Update child key (remove common prefix)
                old_suffix = child.key[i:]
                child.key = old_suffix

                # Add old child to new node
                new_node.children[old_suffix[0]] = child

                # Add new node to parent
                node.children[matched_char] = new_node

                # Add new leaf if there's remaining text
                remaining = remaining[i:]
                if remaining:
                    leaf = PatriciaNode(remaining)
                    leaf.is_end_of_word = True
                    leaf.value = value or word
                    new_node.children[remaining[0]] = leaf
                else:
                    new_node.is_end_of_word = True
                    new_node.value = value or word
                return

        node.is_end_of_word = True
        node.value = value or word

    def search(self, word: str) -> bool:
        """Search for exact word."""
        node, remaining = self._find_node(word)
        return node is not None and not remaining and node.is_end_of_word

    def _find_node(self, word: str) -> Tuple[Optional[PatriciaNode], str]:
        """Find node and return remaining unmatched string."""
        node = self.root
        remaining = word

        while remaining:
            matched_char = remaining[0]
            if matched_char not in node.children:
                return None, remaining

            child = node.children[matched_char]

            # Check if remaining matches child.key
            if not remaining.startswith(child.key):
                return None, remaining

            remaining = remaining[len(child.key):]
            node = child

        return node, remaining

# ============================================================================
# SUFFIX TRIE
# ============================================================================

class SuffixTrie:
    """
    Suffix Trie for pattern matching.

    Stores all suffixes of a text for efficient pattern search.

    Applications:
    - Substring search
    - Pattern matching
    - DNA sequence analysis
    """

    def __init__(self, text: str):
        self.trie = Trie()
        self.text = text

        # Insert all suffixes
        for i in range(len(text)):
            self.trie.insert(text[i:])

    def contains_substring(self, pattern: str) -> bool:
        """Check if pattern exists as substring."""
        return self.trie.starts_with(pattern)

    def find_all_occurrences(self, pattern: str) -> List[int]:
        """Find all starting positions of pattern in text."""
        positions = []

        for i in range(len(self.text)):
            if self.text[i:].startswith(pattern):
                positions.append(i)

        return positions

# ============================================================================
# APPLICATIONS
# ============================================================================

class SpellChecker:
    """
    Spell checker using trie.

    Features:
    - Dictionary lookup
    - Suggestions for misspelled words
    - Edit distance calculations
    """

    def __init__(self, dictionary: List[str]):
        self.trie = Trie()
        for word in dictionary:
            self.trie.insert(word.lower())

    def is_correct(self, word: str) -> bool:
        """Check if word is spelled correctly."""
        return self.trie.search(word.lower())

    def suggest(self, word: str, max_distance: int = 2) -> List[str]:
        """Suggest corrections for misspelled word."""
        word = word.lower()

        if self.is_correct(word):
            return [word]

        suggestions = set()

        # Generate candidates with edit distance 1
        # (deletions, transpositions, replacements, insertions)
        candidates = self._generate_candidates(word, max_distance)

        for candidate in candidates:
            if self.trie.search(candidate):
                suggestions.add(candidate)

        return sorted(suggestions)[:10]

    def _generate_candidates(self, word: str, max_distance: int) -> Set[str]:
        """Generate candidate words within edit distance."""
        if max_distance == 0:
            return {word}

        candidates = {word}
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        # Deletions
        for i in range(len(word)):
            candidates.add(word[:i] + word[i+1:])

        # Transpositions
        for i in range(len(word) - 1):
            candidates.add(word[:i] + word[i+1] + word[i] + word[i+2:])

        # Replacements
        for i in range(len(word)):
            for c in alphabet:
                candidates.add(word[:i] + c + word[i+1:])

        # Insertions
        for i in range(len(word) + 1):
            for c in alphabet:
                candidates.add(word[:i] + c + word[i:])

        if max_distance > 1:
            new_candidates = set()
            for candidate in candidates:
                new_candidates.update(self._generate_candidates(candidate, max_distance - 1))
            candidates.update(new_candidates)

        return candidates

class AutoComplete:
    """
    Auto-complete system using trie.

    Features:
    - Prefix-based suggestions
    - Frequency-based ranking
    - Recent searches boost
    """

    def __init__(self):
        self.trie = Trie()
        self.recent_searches = deque(maxlen=100)

    def add_word(self, word: str, frequency: int = 1):
        """Add word to auto-complete dictionary."""
        self.trie.insert(word.lower(), frequency)

    def search(self, prefix: str) -> List[str]:
        """Get auto-complete suggestions."""
        prefix = prefix.lower()
        suggestions = self.trie.autocomplete(prefix, limit=10)

        # Boost recent searches
        recent_set = set(self.recent_searches)
        boosted = []

        for word, freq in suggestions:
            boost = 2 if word in recent_set else 1
            boosted.append((word, freq * boost))

        boosted.sort(key=lambda x: (-x[1], x[0]))
        return [word for word, _ in boosted]

    def record_search(self, query: str):
        """Record user search for boosting."""
        self.recent_searches.append(query.lower())

class Dictionary:
    """
    Dictionary implementation using trie.

    Features:
    - Fast lookup
    - Prefix search
    - Range queries
    """

    def __init__(self):
        self.trie = PatriciaTrie()

    def add(self, word: str, definition: str):
        """Add word with definition."""
        self.trie.insert(word.lower(), definition)

    def lookup(self, word: str) -> Optional[str]:
        """Get definition for word."""
        node, remaining = self.trie._find_node(word.lower())
        if node and not remaining and node.is_end_of_word:
            return node.value
        return None

    def words_starting_with(self, prefix: str) -> List[str]:
        """Get all words starting with prefix."""
        # For simplicity, using standard trie approach
        trie = Trie()

        def collect_words(node, current):
            if hasattr(node, 'is_end_of_word') and node.is_end_of_word:
                trie.insert(current)
            if hasattr(node, 'children'):
                for char, child in node.children.items():
                    collect_words(child, current + (child.key if hasattr(child, 'key') else char))

        collect_words(self.trie.root, "")
        return [w for w in trie.get_all_words() if w.startswith(prefix.lower())]

# ============================================================================
# PERFORMANCE COMPARISON
# ============================================================================

def performance_comparison():
    """Compare trie with other data structures."""
    import time

    # Test data
    words = ["the", "a", "there", "answer", "any", "by", "bye", "their",
             "abc", "apple", "application", "apply"]

    print("=" * 80)
    print("TRIE vs OTHER DATA STRUCTURES")
    print("=" * 80)

    # Trie
    start = time.time()
    trie = Trie()
    for word in words:
        trie.insert(word)

    # Prefix search
    prefix_results = trie.autocomplete("app")
    trie_time = time.time() - start

    # Hash Set
    start = time.time()
    hash_set = set(words)

    # Prefix search (inefficient)
    prefix_results_hash = [w for w in hash_set if w.startswith("app")]
    hash_time = time.time() - start

    # Sorted List
    start = time.time()
    sorted_list = sorted(words)

    # Binary search for prefix (still inefficient)
    prefix_results_list = [w for w in sorted_list if w.startswith("app")]
    list_time = time.time() - start

    print("\nPrefix Search Performance:")
    print(f"Trie:        {trie_time*1000:.4f}ms - {len(prefix_results)} results")
    print(f"Hash Set:    {hash_time*1000:.4f}ms - {len(prefix_results_hash)} results")
    print(f"Sorted List: {list_time*1000:.4f}ms - {len(prefix_results_list)} results")

    print("\nSpace Complexity:")
    print("Trie:        O(ALPHABET_SIZE * N * M)")
    print("Hash Set:    O(N * M)")
    print("Sorted List: O(N * M)")

    print("\nOperations Complexity:")
    print("                 Trie      Hash Set   Sorted List")
    print("Insert:          O(m)      O(m)       O(n*m)")
    print("Search:          O(m)      O(m)       O(log n * m)")
    print("Delete:          O(m)      O(m)       O(n*m)")
    print("Prefix Search:   O(p+k)    O(n*m)     O(n*m)")
    print("\nWhere: n=words, m=avg length, p=prefix length, k=results")

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate():
    """Demonstrate all trie implementations and applications."""

    print("=" * 80)
    print("COMPREHENSIVE TRIE DEMONSTRATIONS")
    print("=" * 80)

    # Standard Trie
    print("\n1. STANDARD TRIE")
    print("-" * 80)
    trie = Trie()

    words = ["the", "a", "there", "answer", "any", "by", "bye", "their"]
    print("Inserting words:", words)
    for word in words:
        trie.insert(word)

    print(f"\nTotal words: {trie.word_count}")
    print(f"Search 'the': {trie.search('the')}")
    print(f"Search 'these': {trie.search('these')}")
    print(f"Starts with 'th': {trie.starts_with('th')}")

    print(f"\nAuto-complete for 'th': {[w for w, _ in trie.autocomplete('th')]}")
    print(f"Longest common prefix: '{trie.longest_common_prefix()}'")
    print(f"Words with prefix 'the': {trie.count_words_with_prefix('the')}")

    # Patricia Trie
    print("\n2. PATRICIA TRIE (Compressed)")
    print("-" * 80)
    ptrie = PatriciaTrie()

    routes = [("192.168.1.0", "Router A"),
              ("192.168.2.0", "Router B"),
              ("192.168.1.1", "Host 1"),
              ("10.0.0.0", "Network B")]

    for ip, dest in routes:
        ptrie.insert(ip, dest)
        print(f"  Added route: {ip} -> {dest}")

    print(f"\nSearch '192.168.1.0': {ptrie.search('192.168.1.0')}")
    print(f"Search '192.168.1.1': {ptrie.search('192.168.1.1')}")

    # Suffix Trie
    print("\n3. SUFFIX TRIE")
    print("-" * 80)
    text = "banana"
    suffix_trie = SuffixTrie(text)

    print(f"Text: '{text}'")
    print(f"Contains 'ana': {suffix_trie.contains_substring('ana')}")
    print(f"Contains 'nan': {suffix_trie.contains_substring('nan')}")
    print(f"Occurrences of 'ana': {suffix_trie.find_all_occurrences('ana')}")

    # Spell Checker
    print("\n4. SPELL CHECKER")
    print("-" * 80)
    dictionary = ["hello", "world", "python", "programming", "algorithm"]
    checker = SpellChecker(dictionary)

    test_words = ["hello", "helo", "wrld", "python", "pyton"]
    for word in test_words:
        correct = checker.is_correct(word)
        suggestions = checker.suggest(word) if not correct else []
        print(f"  '{word}': {'✓' if correct else '✗'}", end="")
        if suggestions:
            print(f" → Suggestions: {suggestions[:3]}")
        else:
            print()

    # Auto-Complete
    print("\n5. AUTO-COMPLETE")
    print("-" * 80)
    autocomplete = AutoComplete()

    # Add popular searches
    searches = [("python", 100), ("programming", 80), ("program", 60),
                ("javascript", 90), ("java", 95)]

    for word, freq in searches:
        autocomplete.add_word(word, freq)

    print("Popular searches added")
    print(f"\nSuggestions for 'pro': {autocomplete.search('pro')}")
    print(f"Suggestions for 'ja': {autocomplete.search('ja')}")

    # Dictionary
    print("\n6. DICTIONARY")
    print("-" * 80)
    dictionary = Dictionary()

    dictionary.add("algorithm", "A step-by-step procedure for solving a problem")
    dictionary.add("data structure", "A way of organizing data")
    dictionary.add("trie", "A tree-like data structure for storing strings")

    print(f"Lookup 'trie': {dictionary.lookup('trie')}")
    print(f"Lookup 'algorithm': {dictionary.lookup('algorithm')}")

    print("\n" + "=" * 80)
    print("✨ All demonstrations complete!")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate()
    print()
    performance_comparison()
