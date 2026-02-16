/**
 * Text Analysis Example
 * Demonstrates string algorithms for text processing and analysis
 */

import * as stringAlgs from '../src/stringAlgorithms.js';
import { Trie } from '../src/dataStructures.js';

console.log('=== TEXT ANALYSIS EXAMPLE ===\n');

// Sample text for analysis
const document = `
The quick brown fox jumps over the lazy dog.
The dog was not really lazy, just tired.
A quick brown fox is a fast fox indeed.
`;

const searchPatterns = ['fox', 'dog', 'quick', 'slow'];

console.log('Document to analyze:');
console.log(document);
console.log('\n--- Pattern Matching Analysis ---\n');

// Use different string matching algorithms
for (const pattern of searchPatterns) {
    console.log(`Searching for "${pattern}":`);

    // KMP Search
    const kmpResult = stringAlgs.kmpSearch(document, pattern);
    console.log(`  KMP found at positions: ${kmpResult.length > 0 ? kmpResult.join(', ') : 'Not found'}`);

    // Rabin-Karp Search
    const rkResult = stringAlgs.rabinKarpSearch(document, pattern);
    console.log(`  Rabin-Karp found at positions: ${rkResult.length > 0 ? rkResult.join(', ') : 'Not found'}`);

    // Boyer-Moore Search
    const bmResult = stringAlgs.boyerMooreSearch(document, pattern);
    console.log(`  Boyer-Moore found at positions: ${bmResult.length > 0 ? bmResult.join(', ') : 'Not found'}`);

    console.log('');
}

// Spell checker example
console.log('\n--- SPELL CHECKER EXAMPLE ---\n');

const dictionary = ['quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog',
                   'the', 'was', 'not', 'really', 'just', 'tired', 'fast', 'indeed'];

// Build a Trie for efficient dictionary lookup
const dictTrie = new Trie();
dictionary.forEach(word => dictTrie.insert(word.toLowerCase()));

console.log('Dictionary loaded with', dictionary.length, 'words\n');

// Words to check
const wordsToCheck = ['quik', 'brwn', 'foxx', 'jump', 'laxy', 'doog'];

console.log('Spell checking and suggesting corrections:\n');

for (const word of wordsToCheck) {
    const lowercaseWord = word.toLowerCase();

    if (dictTrie.search(lowercaseWord)) {
        console.log(`✓ "${word}" is spelled correctly`);
    } else {
        console.log(`✗ "${word}" might be misspelled`);

        // Find suggestions using edit distance
        const suggestions = [];
        for (const dictWord of dictionary) {
            const distance = stringAlgs.levenshteinDistance(lowercaseWord, dictWord.toLowerCase());
            if (distance <= 2) { // Within 2 edits
                suggestions.push({ word: dictWord, distance });
            }
        }

        // Sort by edit distance
        suggestions.sort((a, b) => a.distance - b.distance);

        if (suggestions.length > 0) {
            console.log(`  Suggestions: ${suggestions.slice(0, 3).map(s => s.word).join(', ')}`);
        }
    }
}

// Palindrome analysis
console.log('\n\n--- PALINDROME ANALYSIS ---\n');

const phrases = [
    'racecar',
    'A man a plan a canal Panama',
    'hello world',
    'Was it a rat I saw',
    'Never odd or even'
];

for (const phrase of phrases) {
    const cleanPhrase = phrase.toLowerCase().replace(/[^a-z]/g, '');
    const isPalindrome = stringAlgs.isPalindrome(cleanPhrase);
    console.log(`"${phrase}"`);
    console.log(`  Clean: "${cleanPhrase}"`);
    console.log(`  Is palindrome: ${isPalindrome ? 'Yes' : 'No'}`);

    if (!isPalindrome) {
        // Find longest palindromic substring
        const longest = stringAlgs.longestPalindromicSubstring(cleanPhrase);
        console.log(`  Longest palindrome within: "${longest}"`);
    }
    console.log('');
}

// Text similarity analysis
console.log('\n--- TEXT SIMILARITY ANALYSIS ---\n');

const sentences = [
    'The quick brown fox',
    'The fast brown fox',
    'A quick red fox',
    'The lazy dog sleeps',
    'Quick foxes jump high'
];

console.log('Comparing sentence similarities:\n');

for (let i = 0; i < sentences.length; i++) {
    for (let j = i + 1; j < sentences.length; j++) {
        const s1 = sentences[i].toLowerCase();
        const s2 = sentences[j].toLowerCase();

        // Calculate edit distance
        const editDist = stringAlgs.levenshteinDistance(s1, s2);

        // Calculate LCS
        const lcs = stringAlgs.longestCommonSubsequence(s1, s2);

        // Similarity score (normalized)
        const maxLen = Math.max(s1.length, s2.length);
        const similarity = ((maxLen - editDist) / maxLen * 100).toFixed(1);

        console.log(`"${sentences[i]}" vs "${sentences[j]}"`);
        console.log(`  Edit distance: ${editDist}`);
        console.log(`  Longest common subsequence: "${lcs}" (length: ${lcs.length})`);
        console.log(`  Similarity: ${similarity}%`);
        console.log('');
    }
}

// Autocomplete example
console.log('\n--- AUTOCOMPLETE SYSTEM ---\n');

const searchTerms = [
    'javascript',
    'java',
    'python',
    'pythonic',
    'rust',
    'ruby',
    'typescript',
    'swift',
    'scala',
    'scheme'
];

const autocompleteTrie = new Trie();
searchTerms.forEach(term => autocompleteTrie.insert(term));

const prefixes = ['ja', 'py', 'r', 's', 'typ'];

console.log('Search terms database:', searchTerms.join(', '));
console.log('\nAutocomplete suggestions:\n');

for (const prefix of prefixes) {
    const suggestions = autocompleteTrie.findWordsWithPrefix(prefix);
    console.log(`"${prefix}" → ${suggestions.length > 0 ? suggestions.join(', ') : 'No suggestions'}`);
}

console.log('\n=== Example completed successfully ===');