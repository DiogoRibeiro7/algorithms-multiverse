"""
String Compression Algorithms
==============================

This module implements various string compression algorithms.

Algorithms:
1. Run-Length Encoding (RLE)
2. LZ77 (Lempel-Ziv 1977)
3. Huffman Coding
4. Burrows-Wheeler Transform (BWT)

Applications:
- Data compression
- File compression
- Network data transmission
- Image compression (PNG uses similar techniques)
- Text processing

Features:
- Compression and decompression
- Compression ratio analysis
- Comparison of different algorithms
"""

from typing import List, Tuple, Dict, Optional
import heapq
from collections import Counter, defaultdict


class RunLengthEncoding:
    """
    Run-Length Encoding (RLE) - Simple compression for repeated characters.

    Time: O(n)
    Space: O(n)

    Best for: Data with long runs of repeated characters
    """

    @staticmethod
    def compress(text: str) -> str:
        """
        Compress using run-length encoding.

        Format: <count><character>
        Example: "aaabbc" -> "3a2b1c"

        Returns compressed string.
        """
        if not text:
            return ""

        compressed = []
        count = 1
        prev_char = text[0]

        for i in range(1, len(text)):
            if text[i] == prev_char:
                count += 1
            else:
                compressed.append(f"{count}{prev_char}")
                prev_char = text[i]
                count = 1

        # Add last run
        compressed.append(f"{count}{prev_char}")

        result = ''.join(compressed)

        # Return original if compression doesn't help
        return result if len(result) < len(text) else text

    @staticmethod
    def decompress(compressed: str) -> str:
        """
        Decompress RLE encoded string.

        Time: O(n * max_count)
        """
        if not compressed:
            return ""

        result = []
        i = 0

        while i < len(compressed):
            # Read count
            count_str = ""
            while i < len(compressed) and compressed[i].isdigit():
                count_str += compressed[i]
                i += 1

            if not count_str:
                break

            count = int(count_str)

            # Read character
            if i < len(compressed):
                char = compressed[i]
                result.append(char * count)
                i += 1

        return ''.join(result)

    @staticmethod
    def compress_binary(data: bytes) -> bytes:
        """
        RLE for binary data.

        Format: <count><byte>
        """
        if not data:
            return b""

        compressed = bytearray()
        count = 1
        prev_byte = data[0]

        for i in range(1, len(data)):
            if data[i] == prev_byte and count < 255:
                count += 1
            else:
                compressed.append(count)
                compressed.append(prev_byte)
                prev_byte = data[i]
                count = 1

        # Add last run
        compressed.append(count)
        compressed.append(prev_byte)

        return bytes(compressed)

    @staticmethod
    def decompress_binary(compressed: bytes) -> bytes:
        """
        Decompress binary RLE.
        """
        if not compressed or len(compressed) % 2 != 0:
            return b""

        result = bytearray()

        for i in range(0, len(compressed), 2):
            count = compressed[i]
            byte = compressed[i + 1]
            result.extend([byte] * count)

        return bytes(result)


class LZ77:
    """
    LZ77 Compression Algorithm (Lempel-Ziv 1977)

    Uses a sliding window to find repeated sequences.

    Time: O(n * window_size)
    Space: O(window_size)

    Applications:
    - DEFLATE (used in ZIP, gzip)
    - PNG compression
    - General purpose compression
    """

    def __init__(self, window_size: int = 4096, lookahead_size: int = 18):
        """
        Initialize LZ77 compressor.

        Args:
            window_size: Size of search buffer (default 4096)
            lookahead_size: Size of lookahead buffer (default 18)
        """
        self.window_size = window_size
        self.lookahead_size = lookahead_size

    def compress(self, text: str, visualize: bool = False) -> List[Tuple[int, int, str]]:
        """
        Compress text using LZ77.

        Returns: List of (offset, length, next_char) tuples

        Format:
        - offset: Distance back to start of match
        - length: Length of match
        - next_char: Character after match

        Example:
        "abcabcabc" -> [(0, 0, 'a'), (0, 0, 'b'), (0, 0, 'c'),
                        (3, 3, 'a'), (6, 3, '')]
        """
        result = []
        i = 0

        if visualize:
            print(f"\nLZ77 Compression (window={self.window_size}, lookahead={self.lookahead_size})")
            print("=" * 70)

        while i < len(text):
            # Search window starts at max(0, i - window_size)
            search_start = max(0, i - self.window_size)
            search_buffer = text[search_start:i]

            # Lookahead buffer
            lookahead_end = min(i + self.lookahead_size, len(text))
            lookahead_buffer = text[i:lookahead_end]

            # Find longest match
            best_offset = 0
            best_length = 0

            for j in range(len(search_buffer)):
                # Match length
                length = 0
                while (length < len(lookahead_buffer) and
                       length < len(search_buffer) - j and
                       search_buffer[j + length] == lookahead_buffer[length]):
                    length += 1

                if length > best_length:
                    best_length = length
                    best_offset = len(search_buffer) - j

            # Get next character
            if best_length < len(lookahead_buffer):
                next_char = lookahead_buffer[best_length]
            else:
                next_char = ''

            result.append((best_offset, best_length, next_char))

            if visualize:
                print(f"Position {i}: offset={best_offset}, length={best_length}, next='{next_char}'")
                if best_length > 0:
                    match_start = i - best_offset
                    print(f"  Match: '{text[match_start:match_start + best_length]}'")

            i += best_length + (1 if next_char else 0)

        return result

    def decompress(self, compressed: List[Tuple[int, int, str]]) -> str:
        """
        Decompress LZ77 encoded data.

        Args:
            compressed: List of (offset, length, next_char) tuples

        Returns: Original text
        """
        result = []

        for offset, length, next_char in compressed:
            if length > 0:
                # Copy from earlier position
                start = len(result) - offset
                for i in range(length):
                    result.append(result[start + i])

            if next_char:
                result.append(next_char)

        return ''.join(result)


class HuffmanCoding:
    """
    Huffman Coding - Optimal prefix-free encoding.

    Time: O(n log n)
    Space: O(n)

    Creates variable-length codes based on character frequency.
    More frequent characters get shorter codes.
    """

    class Node:
        """Binary tree node used to represent Huffman coding states."""

        def __init__(self, char: Optional[str], freq: int, left=None, right=None):
            self.char = char
            self.freq = freq
            self.left = left
            self.right = right

        def __lt__(self, other):
            return self.freq < other.freq

    def build_tree(self, text: str) -> 'HuffmanCoding.Node':
        """
        Build Huffman tree from text.

        Returns: Root node of Huffman tree
        """
        # Count frequencies
        freq = Counter(text)

        # Build priority queue
        heap = [self.Node(char, count) for char, count in freq.items()]
        heapq.heapify(heap)

        # Build tree
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            parent = self.Node(None, left.freq + right.freq, left, right)
            heapq.heappush(heap, parent)

        return heap[0] if heap else None

    def build_codes(self, root: 'HuffmanCoding.Node') -> Dict[str, str]:
        """
        Build Huffman codes from tree.

        Returns: Dictionary mapping characters to binary codes
        """
        codes = {}

        def traverse(node, code):
            if node:
                if node.char is not None:
                    codes[node.char] = code if code else '0'
                else:
                    traverse(node.left, code + '0')
                    traverse(node.right, code + '1')

        traverse(root, '')
        return codes

    def compress(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Compress text using Huffman coding.

        Returns: (compressed_bits, code_table)
        """
        if not text:
            return "", {}

        # Build tree and codes
        root = self.build_tree(text)
        codes = self.build_codes(root)

        # Encode text
        compressed = ''.join(codes[char] for char in text)

        return compressed, codes

    def decompress(self, compressed: str, codes: Dict[str, str]) -> str:
        """
        Decompress Huffman encoded data.

        Args:
            compressed: Binary string
            codes: Code table from compression

        Returns: Original text
        """
        if not compressed:
            return ""

        # Reverse code table
        reverse_codes = {code: char for char, code in codes.items()}

        result = []
        current_code = ""

        for bit in compressed:
            current_code += bit
            if current_code in reverse_codes:
                result.append(reverse_codes[current_code])
                current_code = ""

        return ''.join(result)


class BurrowsWheelerTransform:
    """
    Burrows-Wheeler Transform (BWT)

    Not a compression algorithm itself, but transforms data to make
    it more compressible.

    Time: O(n² log n) or O(n) with suffix array
    Space: O(n²) or O(n) with suffix array

    Used in bzip2 compression.
    """

    @staticmethod
    def transform(text: str) -> Tuple[str, int]:
        """
        Apply Burrows-Wheeler Transform.

        Returns: (transformed_text, original_index)

        Algorithm:
        1. Generate all rotations of text
        2. Sort rotations lexicographically
        3. Take last column
        """
        # Add end marker
        text = text + '$'
        n = len(text)

        # Generate all rotations
        rotations = [text[i:] + text[:i] for i in range(n)]

        # Sort rotations
        rotations.sort()

        # Find original index
        original_index = rotations.index(text)

        # Take last column
        bwt = ''.join(rotation[-1] for rotation in rotations)

        return bwt, original_index

    @staticmethod
    def inverse_transform(bwt: str, original_index: int) -> str:
        """
        Reverse Burrows-Wheeler Transform.

        Args:
            bwt: BWT transformed string
            original_index: Index of original string in sorted rotations

        Returns: Original text
        """
        n = len(bwt)

        # Build table
        table = [''] * n
        for _ in range(n):
            table = sorted(bwt[i] + table[i] for i in range(n))

        # Get original text
        result = table[original_index]

        # Remove end marker
        return result[:-1] if result.endswith('$') else result


class CompressionAnalyzer:
    """
    Analyze and compare compression algorithms.
    """

    @staticmethod
    def compression_ratio(original: str, compressed: str) -> float:
        """
        Calculate compression ratio.

        Returns: original_size / compressed_size
        """
        if not compressed:
            return 0.0

        return len(original) / len(compressed)

    @staticmethod
    def compression_percentage(original: str, compressed: str) -> float:
        """
        Calculate compression percentage.

        Returns: (1 - compressed_size / original_size) * 100
        """
        if not original:
            return 0.0

        return (1 - len(compressed) / len(original)) * 100

    @staticmethod
    def analyze_text(text: str):
        """
        Analyze text for compression suitability.
        """
        print(f"\nText Analysis")
        print("=" * 70)
        print(f"Length: {len(text)}")
        print(f"Unique characters: {len(set(text))}")

        # Character frequency
        freq = Counter(text)
        print(f"\nTop 10 most frequent characters:")
        for char, count in freq.most_common(10):
            char_display = repr(char) if char in '\n\t\r ' else char
            percentage = (count / len(text)) * 100
            print(f"  {char_display:>5} : {count:>6} ({percentage:>5.2f}%)")

        # Entropy
        import math
        entropy = -sum((count / len(text)) * math.log2(count / len(text))
                      for count in freq.values())
        print(f"\nEntropy: {entropy:.4f} bits/character")
        print(f"Theoretical minimum: {len(text) * entropy / 8:.2f} bytes")

    @staticmethod
    def compare_algorithms(text: str):
        """
        Compare different compression algorithms on the same text.
        """
        print(f"\nCompression Algorithm Comparison")
        print("=" * 70)
        print(f"Original size: {len(text)} characters\n")

        # RLE
        rle = RunLengthEncoding()
        rle_compressed = rle.compress(text)
        rle_ratio = CompressionAnalyzer.compression_ratio(text, rle_compressed)
        rle_percent = CompressionAnalyzer.compression_percentage(text, rle_compressed)

        print(f"Run-Length Encoding (RLE):")
        print(f"  Compressed size: {len(rle_compressed)}")
        print(f"  Ratio: {rle_ratio:.4f}")
        print(f"  Space saved: {rle_percent:.2f}%")

        # LZ77
        lz77 = LZ77()
        lz77_compressed = lz77.compress(text)
        # Estimate size (offset: 2 bytes, length: 1 byte, char: 1 byte)
        lz77_size = len(lz77_compressed) * 4
        lz77_ratio = len(text) / lz77_size
        lz77_percent = (1 - lz77_size / len(text)) * 100

        print(f"\nLZ77:")
        print(f"  Compressed tokens: {len(lz77_compressed)}")
        print(f"  Estimated size: {lz77_size} bytes")
        print(f"  Ratio: {lz77_ratio:.4f}")
        print(f"  Space saved: {lz77_percent:.2f}%")

        # Huffman
        huffman = HuffmanCoding()
        huffman_compressed, codes = huffman.compress(text)
        huffman_size = len(huffman_compressed) / 8  # bits to bytes
        huffman_ratio = len(text) / huffman_size
        huffman_percent = (1 - huffman_size / len(text)) * 100

        print(f"\nHuffman Coding:")
        print(f"  Compressed bits: {len(huffman_compressed)}")
        print(f"  Compressed size: {huffman_size:.2f} bytes")
        print(f"  Ratio: {huffman_ratio:.4f}")
        print(f"  Space saved: {huffman_percent:.2f}%")
        print(f"  Code table size: {len(codes)} entries")

        # BWT (just transformation, not compression)
        bwt, idx = BurrowsWheelerTransform.transform(text)
        print(f"\nBurrows-Wheeler Transform:")
        print(f"  Transformed size: {len(bwt)} (same as original)")
        print(f"  Note: BWT is a transformation, not compression")
        print(f"  Makes data more compressible by RLE or Huffman")


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("STRING COMPRESSION ALGORITHMS")
    print("=" * 70)

    # Example 1: Run-Length Encoding
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Run-Length Encoding (RLE)")
    print("=" * 70)

    text = "aaabbbcccaaa"
    rle = RunLengthEncoding()
    compressed = rle.compress(text)
    decompressed = rle.decompress(compressed)

    print(f"Original:     '{text}' ({len(text)} chars)")
    print(f"Compressed:   '{compressed}' ({len(compressed)} chars)")
    print(f"Decompressed: '{decompressed}'")
    print(f"Match: {text == decompressed}")

    # Example 2: LZ77
    print("\n" + "=" * 70)
    print("EXAMPLE 2: LZ77 Compression")
    print("=" * 70)

    text = "abracadabra"
    lz77 = LZ77(window_size=100, lookahead_size=10)
    compressed = lz77.compress(text, visualize=True)
    decompressed = lz77.decompress(compressed)

    print(f"\nOriginal:     '{text}'")
    print(f"Compressed:   {compressed}")
    print(f"Decompressed: '{decompressed}'")
    print(f"Match: {text == decompressed}")

    # Example 3: Huffman Coding
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Huffman Coding")
    print("=" * 70)

    text = "this is an example for huffman encoding"
    huffman = HuffmanCoding()
    compressed, codes = huffman.compress(text)
    decompressed = huffman.decompress(compressed, codes)

    print(f"Original:  '{text}' ({len(text)} chars = {len(text) * 8} bits)")
    print(f"\nHuffman codes:")
    for char, code in sorted(codes.items(), key=lambda x: len(x[1])):
        char_display = repr(char) if char == ' ' else char
        print(f"  {char_display} : {code}")

    print(f"\nCompressed: {len(compressed)} bits ({len(compressed) / 8:.2f} bytes)")
    print(f"Decompressed: '{decompressed}'")
    print(f"Match: {text == decompressed}")
    print(f"Compression ratio: {len(text) * 8 / len(compressed):.2f}")

    # Example 4: Burrows-Wheeler Transform
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Burrows-Wheeler Transform")
    print("=" * 70)

    text = "banana"
    bwt, original_idx = BurrowsWheelerTransform.transform(text)
    recovered = BurrowsWheelerTransform.inverse_transform(bwt, original_idx)

    print(f"Original:   '{text}'")
    print(f"BWT:        '{bwt}'")
    print(f"Index:      {original_idx}")
    print(f"Recovered:  '{recovered}'")
    print(f"Match: {text == recovered}")

    # Show why BWT is useful
    print(f"\nCharacter runs in original: {len(text)}")
    print(f"Character runs in BWT: {len(bwt)}")
    print(f"Notice BWT groups similar characters together!")

    # Example 5: Compression Analysis
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Compression Analysis")
    print("=" * 70)

    text = "the quick brown fox jumps over the lazy dog " * 5
    CompressionAnalyzer.analyze_text(text)

    # Example 6: Algorithm Comparison
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Algorithm Comparison")
    print("=" * 70)

    # Test with repetitive text
    text1 = "a" * 100 + "b" * 100 + "c" * 100
    print("\nTest 1: Highly repetitive text")
    CompressionAnalyzer.compare_algorithms(text1)

    # Test with natural text
    text2 = "to be or not to be that is the question"
    print("\n\nTest 2: Natural text")
    CompressionAnalyzer.compare_algorithms(text2)

    print("\n" + "=" * 70)
