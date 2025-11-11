/**
 * Comprehensive Trie Data Structure Implementations in Go
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

package main

import (
	"fmt"
	"sort"
	"strings"
)

// ============================================================================
// STANDARD TRIE
// ============================================================================

// TrieNode represents a node in a standard trie
type TrieNode struct {
	children    map[rune]*TrieNode
	isEndOfWord bool
	frequency   int // For ranking suggestions
}

// NewTrieNode creates a new trie node
func NewTrieNode() *TrieNode {
	return &TrieNode{
		children:    make(map[rune]*TrieNode),
		isEndOfWord: false,
		frequency:   0,
	}
}

// Trie represents a standard trie implementation
type Trie struct {
	root      *TrieNode
	wordCount int
}

// NewTrie creates a new trie
func NewTrie() *Trie {
	return &Trie{
		root:      NewTrieNode(),
		wordCount: 0,
	}
}

// Insert adds a word into the trie. O(m)
func (t *Trie) Insert(word string, frequency int) {
	node := t.root

	for _, char := range word {
		if _, exists := node.children[char]; !exists {
			node.children[char] = NewTrieNode()
		}
		node = node.children[char]
	}

	if !node.isEndOfWord {
		t.wordCount++
	}

	node.isEndOfWord = true
	node.frequency = frequency
}

// Search looks for an exact word. O(m)
func (t *Trie) Search(word string) bool {
	node := t.findNode(word)
	return node != nil && node.isEndOfWord
}

// StartsWith checks if any word starts with prefix. O(p)
func (t *Trie) StartsWith(prefix string) bool {
	return t.findNode(prefix) != nil
}

// findNode is a helper to find node for given prefix
func (t *Trie) findNode(prefix string) *TrieNode {
	node := t.root

	for _, char := range prefix {
		if _, exists := node.children[char]; !exists {
			return nil
		}
		node = node.children[char]
	}

	return node
}

// Delete removes a word from trie. O(m)
func (t *Trie) Delete(word string) bool {
	return t.deleteHelper(t.root, word, 0)
}

func (t *Trie) deleteHelper(node *TrieNode, word string, index int) bool {
	runes := []rune(word)

	if index == len(runes) {
		if !node.isEndOfWord {
			return false
		}

		node.isEndOfWord = false
		t.wordCount--
		return len(node.children) == 0
	}

	char := runes[index]
	if _, exists := node.children[char]; !exists {
		return false
	}

	child := node.children[char]
	shouldDeleteChild := t.deleteHelper(child, word, index+1)

	if shouldDeleteChild {
		delete(node.children, char)
		return !node.isEndOfWord && len(node.children) == 0
	}

	return false
}

// Suggestion represents an autocomplete suggestion
type Suggestion struct {
	Word      string
	Frequency int
}

// Autocomplete gets word suggestions for prefix
func (t *Trie) Autocomplete(prefix string, limit int) []Suggestion {
	node := t.findNode(prefix)
	if node == nil {
		return []Suggestion{}
	}

	suggestions := []Suggestion{}
	t.dfsCollectWords(node, prefix, &suggestions)

	// Sort by frequency (descending) and then alphabetically
	sort.Slice(suggestions, func(i, j int) bool {
		if suggestions[i].Frequency != suggestions[j].Frequency {
			return suggestions[i].Frequency > suggestions[j].Frequency
		}
		return suggestions[i].Word < suggestions[j].Word
	})

	if len(suggestions) > limit {
		suggestions = suggestions[:limit]
	}

	return suggestions
}

func (t *Trie) dfsCollectWords(node *TrieNode, current string, suggestions *[]Suggestion) {
	if node.isEndOfWord {
		*suggestions = append(*suggestions, Suggestion{
			Word:      current,
			Frequency: node.frequency,
		})
	}

	// Get sorted children for consistent ordering
	chars := make([]rune, 0, len(node.children))
	for char := range node.children {
		chars = append(chars, char)
	}
	sort.Slice(chars, func(i, j int) bool { return chars[i] < chars[j] })

	for _, char := range chars {
		t.dfsCollectWords(node.children[char], current+string(char), suggestions)
	}
}

// LongestCommonPrefix finds longest common prefix of all words
func (t *Trie) LongestCommonPrefix() string {
	if len(t.root.children) == 0 {
		return ""
	}

	prefix := ""
	node := t.root

	for len(node.children) == 1 && !node.isEndOfWord {
		for char, child := range node.children {
			prefix += string(char)
			node = child
			break
		}
	}

	return prefix
}

// GetAllWords returns all words in trie
func (t *Trie) GetAllWords() []string {
	words := []string{}
	t.dfsCollectAllWords(t.root, "", &words)
	sort.Strings(words)
	return words
}

func (t *Trie) dfsCollectAllWords(node *TrieNode, current string, words *[]string) {
	if node.isEndOfWord {
		*words = append(*words, current)
	}

	for char, child := range node.children {
		t.dfsCollectAllWords(child, current+string(char), words)
	}
}

// CountWordsWithPrefix counts how many words have given prefix
func (t *Trie) CountWordsWithPrefix(prefix string) int {
	node := t.findNode(prefix)
	if node == nil {
		return 0
	}

	return t.countWordsHelper(node)
}

func (t *Trie) countWordsHelper(node *TrieNode) int {
	count := 0
	if node.isEndOfWord {
		count = 1
	}

	for _, child := range node.children {
		count += t.countWordsHelper(child)
	}

	return count
}

// GetWordCount returns the total number of words
func (t *Trie) GetWordCount() int {
	return t.wordCount
}

// ============================================================================
// COMPRESSED TRIE (PATRICIA TREE)
// ============================================================================

// PatriciaNode represents a node in Patricia trie
type PatriciaNode struct {
	key         string // Edge label (can be multiple characters)
	children    map[rune]*PatriciaNode
	isEndOfWord bool
	value       string
}

// NewPatriciaNode creates a new Patricia node
func NewPatriciaNode(key string) *PatriciaNode {
	return &PatriciaNode{
		key:         key,
		children:    make(map[rune]*PatriciaNode),
		isEndOfWord: false,
		value:       "",
	}
}

// PatriciaTrie represents a compressed trie
type PatriciaTrie struct {
	root *PatriciaNode
}

// NewPatriciaTrie creates a new Patricia trie
func NewPatriciaTrie() *PatriciaTrie {
	return &PatriciaTrie{
		root: NewPatriciaNode(""),
	}
}

// Insert adds a word into Patricia trie
func (pt *PatriciaTrie) Insert(word, value string) {
	if word == "" {
		return
	}

	node := pt.root
	remaining := word

	for len(remaining) > 0 {
		matchedChar := rune(remaining[0])

		if _, exists := node.children[matchedChar]; !exists {
			// No matching child, create new node
			newNode := NewPatriciaNode(remaining)
			newNode.isEndOfWord = true
			if value == "" {
				newNode.value = word
			} else {
				newNode.value = value
			}
			node.children[matchedChar] = newNode
			return
		}

		child := node.children[matchedChar]

		// Find common prefix between remaining and child.key
		i := 0
		childRunes := []rune(child.key)
		remainingRunes := []rune(remaining)

		for i < len(remainingRunes) && i < len(childRunes) &&
			remainingRunes[i] == childRunes[i] {
			i++
		}

		if i == len(childRunes) {
			// Child key is prefix of remaining
			node = child
			remaining = string(remainingRunes[i:])
		} else {
			// Need to split the edge
			common := string(childRunes[:i])

			// Create new intermediate node
			newNode := NewPatriciaNode(common)

			// Update child key (remove common prefix)
			oldSuffix := string(childRunes[i:])
			child.key = oldSuffix

			// Add old child to new node
			newNode.children[rune(oldSuffix[0])] = child

			// Add new node to parent
			node.children[matchedChar] = newNode

			// Add new leaf if there's remaining text
			remaining = string(remainingRunes[i:])
			if len(remaining) > 0 {
				leaf := NewPatriciaNode(remaining)
				leaf.isEndOfWord = true
				if value == "" {
					leaf.value = word
				} else {
					leaf.value = value
				}
				newNode.children[rune(remaining[0])] = leaf
			} else {
				newNode.isEndOfWord = true
				if value == "" {
					newNode.value = word
				} else {
					newNode.value = value
				}
			}
			return
		}
	}

	node.isEndOfWord = true
	if value == "" {
		node.value = word
	} else {
		node.value = value
	}
}

// Search looks for an exact word
func (pt *PatriciaTrie) Search(word string) bool {
	node := pt.findNode(word)
	return node != nil && node.isEndOfWord
}

// findNode is a helper to find node for given word
func (pt *PatriciaTrie) findNode(word string) *PatriciaNode {
	node := pt.root
	remaining := word

	for len(remaining) > 0 {
		matchedChar := rune(remaining[0])
		if _, exists := node.children[matchedChar]; !exists {
			return nil
		}

		child := node.children[matchedChar]

		// Check if remaining matches child.key
		if !strings.HasPrefix(remaining, child.key) {
			return nil
		}

		remaining = remaining[len(child.key):]
		node = child
	}

	if len(remaining) == 0 {
		return node
	}
	return nil
}

// GetValue retrieves the value for a word
func (pt *PatriciaTrie) GetValue(word string) string {
	node := pt.findNode(word)
	if node != nil && node.isEndOfWord {
		return node.value
	}
	return ""
}

// ============================================================================
// SUFFIX TRIE
// ============================================================================

// SuffixTrie represents a suffix trie
type SuffixTrie struct {
	trie *Trie
	text string
}

// NewSuffixTrie creates a new suffix trie
func NewSuffixTrie(text string) *SuffixTrie {
	st := &SuffixTrie{
		trie: NewTrie(),
		text: text,
	}

	// Insert all suffixes
	for i := range text {
		st.trie.Insert(text[i:], 1)
	}

	return st
}

// ContainsSubstring checks if pattern exists as substring
func (st *SuffixTrie) ContainsSubstring(pattern string) bool {
	return st.trie.StartsWith(pattern)
}

// FindAllOccurrences finds all starting positions of pattern in text
func (st *SuffixTrie) FindAllOccurrences(pattern string) []int {
	positions := []int{}

	for i := range st.text {
		if strings.HasPrefix(st.text[i:], pattern) {
			positions = append(positions, i)
		}
	}

	return positions
}

// ============================================================================
// APPLICATIONS
// ============================================================================

// SpellChecker implements spell checking using trie
type SpellChecker struct {
	trie *Trie
}

// NewSpellChecker creates a new spell checker
func NewSpellChecker(dictionary []string) *SpellChecker {
	sc := &SpellChecker{
		trie: NewTrie(),
	}

	for _, word := range dictionary {
		sc.trie.Insert(strings.ToLower(word), 1)
	}

	return sc
}

// IsCorrect checks if word is spelled correctly
func (sc *SpellChecker) IsCorrect(word string) bool {
	return sc.trie.Search(strings.ToLower(word))
}

// Suggest provides corrections for misspelled word
func (sc *SpellChecker) Suggest(word string, maxDistance int) []string {
	word = strings.ToLower(word)

	if sc.IsCorrect(word) {
		return []string{word}
	}

	suggestions := make(map[string]bool)
	candidates := sc.generateCandidates(word, maxDistance)

	for candidate := range candidates {
		if sc.trie.Search(candidate) {
			suggestions[candidate] = true
		}
	}

	result := make([]string, 0, len(suggestions))
	for s := range suggestions {
		result = append(result, s)
	}
	sort.Strings(result)

	if len(result) > 10 {
		result = result[:10]
	}

	return result
}

func (sc *SpellChecker) generateCandidates(word string, maxDistance int) map[string]bool {
	if maxDistance == 0 {
		return map[string]bool{word: true}
	}

	candidates := make(map[string]bool)
	candidates[word] = true
	alphabet := "abcdefghijklmnopqrstuvwxyz"

	runes := []rune(word)

	// Deletions
	for i := range runes {
		candidates[string(runes[:i])+string(runes[i+1:])] = true
	}

	// Transpositions
	for i := 0; i < len(runes)-1; i++ {
		transposed := string(runes[:i]) + string(runes[i+1]) +
			string(runes[i]) + string(runes[i+2:])
		candidates[transposed] = true
	}

	// Replacements
	for i := range runes {
		for _, c := range alphabet {
			candidates[string(runes[:i])+string(c)+string(runes[i+1:])] = true
		}
	}

	// Insertions
	for i := 0; i <= len(runes); i++ {
		for _, c := range alphabet {
			candidates[string(runes[:i])+string(c)+string(runes[i:])] = true
		}
	}

	if maxDistance > 1 {
		newCandidates := make(map[string]bool)
		for candidate := range candidates {
			recursive := sc.generateCandidates(candidate, maxDistance-1)
			for rc := range recursive {
				newCandidates[rc] = true
			}
		}
		for nc := range newCandidates {
			candidates[nc] = true
		}
	}

	return candidates
}

// AutoComplete implements auto-complete system
type AutoComplete struct {
	trie           *Trie
	recentSearches []string
	maxRecent      int
}

// NewAutoComplete creates a new auto-complete system
func NewAutoComplete() *AutoComplete {
	return &AutoComplete{
		trie:           NewTrie(),
		recentSearches: []string{},
		maxRecent:      100,
	}
}

// AddWord adds a word to auto-complete dictionary
func (ac *AutoComplete) AddWord(word string, frequency int) {
	ac.trie.Insert(strings.ToLower(word), frequency)
}

// Search gets auto-complete suggestions
func (ac *AutoComplete) Search(prefix string) []string {
	prefix = strings.ToLower(prefix)
	suggestions := ac.trie.Autocomplete(prefix, 10)

	// Boost recent searches
	recentSet := make(map[string]bool)
	for _, s := range ac.recentSearches {
		recentSet[s] = true
	}

	boosted := make([]Suggestion, len(suggestions))
	for i, s := range suggestions {
		freq := s.Frequency
		if recentSet[s.Word] {
			freq *= 2
		}
		boosted[i] = Suggestion{Word: s.Word, Frequency: freq}
	}

	sort.Slice(boosted, func(i, j int) bool {
		if boosted[i].Frequency != boosted[j].Frequency {
			return boosted[i].Frequency > boosted[j].Frequency
		}
		return boosted[i].Word < boosted[j].Word
	})

	result := make([]string, len(boosted))
	for i, s := range boosted {
		result[i] = s.Word
	}

	return result
}

// RecordSearch records user search for boosting
func (ac *AutoComplete) RecordSearch(query string) {
	ac.recentSearches = append(ac.recentSearches, strings.ToLower(query))
	if len(ac.recentSearches) > ac.maxRecent {
		ac.recentSearches = ac.recentSearches[1:]
	}
}

// Dictionary implements dictionary using trie
type Dictionary struct {
	trie *PatriciaTrie
}

// NewDictionary creates a new dictionary
func NewDictionary() *Dictionary {
	return &Dictionary{
		trie: NewPatriciaTrie(),
	}
}

// Add adds a word with definition
func (d *Dictionary) Add(word, definition string) {
	d.trie.Insert(strings.ToLower(word), definition)
}

// Lookup gets definition for word
func (d *Dictionary) Lookup(word string) string {
	return d.trie.GetValue(strings.ToLower(word))
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

func demonstrate() {
	fmt.Println(strings.Repeat("=", 80))
	fmt.Println("COMPREHENSIVE TRIE DEMONSTRATIONS")
	fmt.Println(strings.Repeat("=", 80))

	// Standard Trie
	fmt.Println("\n1. STANDARD TRIE")
	fmt.Println(strings.Repeat("-", 80))
	trie := NewTrie()

	words := []string{"the", "a", "there", "answer", "any", "by", "bye", "their"}
	fmt.Printf("Inserting words: %s\n", strings.Join(words, ", "))
	for _, word := range words {
		trie.Insert(word, 1)
	}

	fmt.Printf("\nTotal words: %d\n", trie.GetWordCount())
	fmt.Printf("Search 'the': %t\n", trie.Search("the"))
	fmt.Printf("Search 'these': %t\n", trie.Search("these"))
	fmt.Printf("Starts with 'th': %t\n", trie.StartsWith("th"))

	autocomplete := trie.Autocomplete("th", 10)
	autocompleteWords := make([]string, len(autocomplete))
	for i, s := range autocomplete {
		autocompleteWords[i] = s.Word
	}
	fmt.Printf("\nAuto-complete for 'th': %s\n", strings.Join(autocompleteWords, ", "))
	fmt.Printf("Longest common prefix: '%s'\n", trie.LongestCommonPrefix())
	fmt.Printf("Words with prefix 'the': %d\n", trie.CountWordsWithPrefix("the"))

	// Patricia Trie
	fmt.Println("\n2. PATRICIA TRIE (Compressed)")
	fmt.Println(strings.Repeat("-", 80))
	ptrie := NewPatriciaTrie()

	routes := [][2]string{
		{"192.168.1.0", "Router A"},
		{"192.168.2.0", "Router B"},
		{"192.168.1.1", "Host 1"},
		{"10.0.0.0", "Network B"},
	}

	for _, route := range routes {
		ptrie.Insert(route[0], route[1])
		fmt.Printf("  Added route: %s -> %s\n", route[0], route[1])
	}

	fmt.Printf("\nSearch '192.168.1.0': %t\n", ptrie.Search("192.168.1.0"))
	fmt.Printf("Search '192.168.1.1': %t\n", ptrie.Search("192.168.1.1"))

	// Suffix Trie
	fmt.Println("\n3. SUFFIX TRIE")
	fmt.Println(strings.Repeat("-", 80))
	text := "banana"
	suffixTrie := NewSuffixTrie(text)

	fmt.Printf("Text: '%s'\n", text)
	fmt.Printf("Contains 'ana': %t\n", suffixTrie.ContainsSubstring("ana"))
	fmt.Printf("Contains 'nan': %t\n", suffixTrie.ContainsSubstring("nan"))
	occurrences := suffixTrie.FindAllOccurrences("ana")
	fmt.Printf("Occurrences of 'ana': %v\n", occurrences)

	// Spell Checker
	fmt.Println("\n4. SPELL CHECKER")
	fmt.Println(strings.Repeat("-", 80))
	dictionary := []string{"hello", "world", "python", "programming", "algorithm"}
	checker := NewSpellChecker(dictionary)

	testWords := []string{"hello", "helo", "wrld", "python", "pyton"}
	for _, word := range testWords {
		correct := checker.IsCorrect(word)
		var suggestions []string
		if !correct {
			suggestions = checker.Suggest(word, 2)
		}
		fmt.Printf("  '%s': %s", word, map[bool]string{true: "✓", false: "✗"}[correct])
		if len(suggestions) > 0 {
			if len(suggestions) > 3 {
				suggestions = suggestions[:3]
			}
			fmt.Printf(" → Suggestions: %s", strings.Join(suggestions, ", "))
		}
		fmt.Println()
	}

	// Auto-Complete
	fmt.Println("\n5. AUTO-COMPLETE")
	fmt.Println(strings.Repeat("-", 80))
	autoComplete := NewAutoComplete()

	searches := [][2]interface{}{
		{"python", 100},
		{"programming", 80},
		{"program", 60},
		{"javascript", 90},
		{"java", 95},
	}

	for _, search := range searches {
		autoComplete.AddWord(search[0].(string), search[1].(int))
	}

	fmt.Println("Popular searches added")
	fmt.Printf("\nSuggestions for 'pro': %s\n", strings.Join(autoComplete.Search("pro"), ", "))
	fmt.Printf("Suggestions for 'ja': %s\n", strings.Join(autoComplete.Search("ja"), ", "))

	// Dictionary
	fmt.Println("\n6. DICTIONARY")
	fmt.Println(strings.Repeat("-", 80))
	dict := NewDictionary()

	dict.Add("algorithm", "A step-by-step procedure for solving a problem")
	dict.Add("data structure", "A way of organizing data")
	dict.Add("trie", "A tree-like data structure for storing strings")

	fmt.Printf("Lookup 'trie': %s\n", dict.Lookup("trie"))
	fmt.Printf("Lookup 'algorithm': %s\n", dict.Lookup("algorithm"))

	fmt.Println("\n" + strings.Repeat("=", 80))
	fmt.Println("✨ All demonstrations complete!")
	fmt.Println(strings.Repeat("=", 80))
}

func main() {
	demonstrate()
}
