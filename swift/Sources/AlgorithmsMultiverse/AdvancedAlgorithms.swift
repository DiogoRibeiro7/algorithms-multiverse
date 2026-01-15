// Advanced Algorithms - Swift Implementation
// Specialized algorithms including compression, cryptography, and computational geometry

import Foundation
import CryptoKit  // For cryptographic operations (iOS 13+)

/// Namespace for advanced and specialized algorithms
public enum AdvancedAlgorithms {

    // MARK: - Compression Algorithms

    /// Huffman coding for text compression
    public class HuffmanCoding {
        /// Node in Huffman tree
        class Node: Comparable {
            let char: Character?
            let frequency: Int
            let left: Node?
            let right: Node?

            init(char: Character? = nil, frequency: Int, left: Node? = nil, right: Node? = nil) {
                self.char = char
                self.frequency = frequency
                self.left = left
                self.right = right
            }

            static func < (lhs: Node, rhs: Node) -> Bool {
                return lhs.frequency < rhs.frequency
            }

            static func == (lhs: Node, rhs: Node) -> Bool {
                return lhs.frequency == rhs.frequency
            }
        }

        /// Encode string using Huffman coding
        public static func encode(_ text: String) -> (encoded: String, tree: Node?) {
            guard !text.isEmpty else { return ("", nil) }

            // Calculate frequency
            var frequency: [Character: Int] = [:]
            for char in text {
                frequency[char, default: 0] += 1
            }

            // Build Huffman tree
            var heap = frequency.map { Node(char: $0.key, frequency: $0.value) }.sorted()

            while heap.count > 1 {
                let left = heap.removeFirst()
                let right = heap.removeFirst()
                let parent = Node(frequency: left.frequency + right.frequency, left: left, right: right)

                // Insert parent back in sorted order
                let insertIndex = heap.firstIndex { $0.frequency >= parent.frequency } ?? heap.count
                heap.insert(parent, at: insertIndex)
            }

            let root = heap.first

            // Generate codes
            var codes: [Character: String] = [:]
            generateCodes(root, "", &codes)

            // Encode text
            var encoded = ""
            for char in text {
                encoded += codes[char] ?? ""
            }

            return (encoded, root)
        }

        private static func generateCodes(_ node: Node?, _ code: String, _ codes: inout [Character: String]) {
            guard let node = node else { return }

            if let char = node.char {
                codes[char] = code.isEmpty ? "0" : code
                return
            }

            generateCodes(node.left, code + "0", &codes)
            generateCodes(node.right, code + "1", &codes)
        }

        /// Decode Huffman-encoded string
        public static func decode(_ encoded: String, tree: Node?) -> String {
            guard let root = tree else { return "" }

            var decoded = ""
            var current = root

            for bit in encoded {
                if bit == "0" {
                    current = current.left ?? root
                } else {
                    current = current.right ?? root
                }

                if let char = current.char {
                    decoded.append(char)
                    current = root
                }
            }

            return decoded
        }
    }

    /// LZW (Lempel-Ziv-Welch) compression
    public struct LZW {
        /// Compress string using LZW
        public static func compress(_ uncompressed: String) -> [Int] {
            var dictionary: [String: Int] = [:]
            for i in 0..<256 {
                dictionary[String(Character(UnicodeScalar(i)!))] = i
            }

            var w = ""
            var compressed: [Int] = []
            var dictSize = 256

            for c in uncompressed {
                let wc = w + String(c)
                if dictionary[wc] != nil {
                    w = wc
                } else {
                    compressed.append(dictionary[w]!)
                    dictionary[wc] = dictSize
                    dictSize += 1
                    w = String(c)
                }
            }

            if !w.isEmpty {
                compressed.append(dictionary[w]!)
            }

            return compressed
        }

        /// Decompress LZW-compressed data
        public static func decompress(_ compressed: [Int]) -> String {
            var dictionary: [Int: String] = [:]
            for i in 0..<256 {
                dictionary[i] = String(Character(UnicodeScalar(i)!))
            }

            guard let first = compressed.first else { return "" }
            var w = dictionary[first]!
            var decompressed = w
            var dictSize = 256

            for k in compressed.dropFirst() {
                let entry: String
                if let existing = dictionary[k] {
                    entry = existing
                } else if k == dictSize {
                    entry = w + String(w.first!)
                } else {
                    return ""  // Invalid compressed data
                }

                decompressed += entry
                dictionary[dictSize] = w + String(entry.first!)
                dictSize += 1
                w = entry
            }

            return decompressed
        }
    }

    // MARK: - Cryptographic Algorithms (Educational)

    /// Caesar cipher (for educational purposes)
    public struct CaesarCipher {
        /// Encrypt text using Caesar cipher
        public static func encrypt(_ text: String, shift: Int) -> String {
            return text.map { char in
                guard char.isLetter else { return char }

                let isUppercase = char.isUppercase
                let baseValue = isUppercase ? 65 : 97
                let shifted = ((Int(char.asciiValue!) - baseValue + shift) % 26 + 26) % 26
                return Character(UnicodeScalar(shifted + baseValue)!)
            }.map(String.init).joined()
        }

        /// Decrypt Caesar cipher
        public static func decrypt(_ text: String, shift: Int) -> String {
            return encrypt(text, shift: -shift)
        }
    }

    /// Vigenère cipher
    public struct VigenereCipher {
        /// Encrypt using Vigenère cipher
        public static func encrypt(_ text: String, key: String) -> String {
            let keyArray = Array(key.uppercased())
            var keyIndex = 0

            return text.map { char in
                guard char.isLetter else { return char }

                let shift = Int(keyArray[keyIndex % keyArray.count].asciiValue!) - 65
                keyIndex += 1

                let isUppercase = char.isUppercase
                let baseValue = isUppercase ? 65 : 97
                let shifted = ((Int(char.asciiValue!) - baseValue + shift) % 26 + 26) % 26
                return Character(UnicodeScalar(shifted + baseValue)!)
            }.map(String.init).joined()
        }

        /// Decrypt Vigenère cipher
        public static func decrypt(_ text: String, key: String) -> String {
            let decryptKey = key.map { char in
                Character(UnicodeScalar(90 - (Int(char.asciiValue!) - 65))!)
            }.map(String.init).joined()
            return encrypt(text, key: decryptKey)
        }
    }

    /// Simple XOR cipher
    public struct XORCipher {
        /// XOR encrypt/decrypt (symmetric)
        public static func process(_ data: Data, key: Data) -> Data {
            var result = Data()

            for (index, byte) in data.enumerated() {
                result.append(byte ^ key[index % key.count])
            }

            return result
        }
    }

    // MARK: - Computational Geometry

    /// Point in 2D space
    public struct Point2D: Equatable {
        public let x: Double
        public let y: Double

        public init(_ x: Double, _ y: Double) {
            self.x = x
            self.y = y
        }

        /// Distance to another point
        public func distance(to other: Point2D) -> Double {
            let dx = x - other.x
            let dy = y - other.y
            return sqrt(dx * dx + dy * dy)
        }
    }

    /// Check if three points are collinear
    public static func areCollinear(_ p1: Point2D, _ p2: Point2D, _ p3: Point2D) -> Bool {
        // Points are collinear if area of triangle is 0
        let area = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)
        return abs(area) < Double.ulpOfOne
    }

    /// Convex hull using Graham Scan
    /// - Complexity: O(n log n) time
    public static func convexHull(_ points: [Point2D]) -> [Point2D] {
        guard points.count >= 3 else { return points }

        // Find starting point (lowest y, then leftmost x)
        let start = points.min { p1, p2 in
            p1.y < p2.y || (p1.y == p2.y && p1.x < p2.x)
        }!

        // Sort points by polar angle with respect to start
        let sorted = points.filter { $0 != start }.sorted { p1, p2 in
            let cross = crossProduct(start, p1, p2)
            if abs(cross) < Double.ulpOfOne {
                // Collinear - sort by distance
                return p1.distance(to: start) < p2.distance(to: start)
            }
            return cross > 0
        }

        // Graham scan
        var hull = [start]

        for point in sorted {
            while hull.count > 1 &&
                  crossProduct(hull[hull.count - 2], hull.last!, point) <= 0 {
                hull.removeLast()
            }
            hull.append(point)
        }

        return hull
    }

    private static func crossProduct(_ origin: Point2D, _ p1: Point2D, _ p2: Point2D) -> Double {
        return (p1.x - origin.x) * (p2.y - origin.y) - (p2.x - origin.x) * (p1.y - origin.y)
    }

    /// Find closest pair of points using divide and conquer
    /// - Complexity: O(n log n) time
    public static func closestPair(_ points: [Point2D]) -> (Point2D, Point2D, Double)? {
        guard points.count >= 2 else { return nil }

        let sortedByX = points.sorted { $0.x < $1.x }
        return closestPairRecursive(sortedByX)
    }

    private static func closestPairRecursive(_ points: [Point2D]) -> (Point2D, Point2D, Double)? {
        let n = points.count

        // Base case: brute force for small arrays
        if n <= 3 {
            var minDist = Double.infinity
            var pair: (Point2D, Point2D)?

            for i in 0..<n {
                for j in i+1..<n {
                    let dist = points[i].distance(to: points[j])
                    if dist < minDist {
                        minDist = dist
                        pair = (points[i], points[j])
                    }
                }
            }

            return pair.map { ($0, $1, minDist) }
        }

        // Divide
        let mid = n / 2
        let midPoint = points[mid]
        let left = Array(points[0..<mid])
        let right = Array(points[mid..<n])

        // Conquer
        let leftResult = closestPairRecursive(left)
        let rightResult = closestPairRecursive(right)

        // Find minimum of left and right
        let minResult: (Point2D, Point2D, Double)?
        if let l = leftResult, let r = rightResult {
            minResult = l.2 < r.2 ? l : r
        } else {
            minResult = leftResult ?? rightResult
        }

        guard let currentMin = minResult else { return nil }

        // Check strip
        let strip = points.filter { abs($0.x - midPoint.x) < currentMin.2 }

        // Find closest in strip
        var stripMin = currentMin
        for i in 0..<strip.count {
            for j in i+1..<strip.count {
                if strip[j].y - strip[i].y >= stripMin.2 {
                    break
                }

                let dist = strip[i].distance(to: strip[j])
                if dist < stripMin.2 {
                    stripMin = (strip[i], strip[j], dist)
                }
            }
        }

        return stripMin
    }

    /// Line segment intersection
    public static func doSegmentsIntersect(
        _ p1: Point2D, _ q1: Point2D,
        _ p2: Point2D, _ q2: Point2D
    ) -> Bool {
        func orientation(_ p: Point2D, _ q: Point2D, _ r: Point2D) -> Int {
            let val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if abs(val) < Double.ulpOfOne { return 0 }  // Collinear
            return val > 0 ? 1 : 2  // Clockwise or Counterclockwise
        }

        func onSegment(_ p: Point2D, _ q: Point2D, _ r: Point2D) -> Bool {
            return q.x <= max(p.x, r.x) && q.x >= min(p.x, r.x) &&
                   q.y <= max(p.y, r.y) && q.y >= min(p.y, r.y)
        }

        let o1 = orientation(p1, q1, p2)
        let o2 = orientation(p1, q1, q2)
        let o3 = orientation(p2, q2, p1)
        let o4 = orientation(p2, q2, q1)

        // General case
        if o1 != o2 && o3 != o4 {
            return true
        }

        // Special cases (collinear)
        if o1 == 0 && onSegment(p1, p2, q1) { return true }
        if o2 == 0 && onSegment(p1, q2, q1) { return true }
        if o3 == 0 && onSegment(p2, p1, q2) { return true }
        if o4 == 0 && onSegment(p2, q1, q2) { return true }

        return false
    }

    // MARK: - Bloom Filter

    /// Probabilistic data structure for membership testing
    public class BloomFilter {
        private var bitArray: [Bool]
        private let size: Int
        private let hashCount: Int

        public init(expectedElements: Int, falsePositiveRate: Double = 0.01) {
            // Calculate optimal size and hash count
            let m = -Double(expectedElements) * log(falsePositiveRate) / pow(log(2), 2)
            self.size = Int(ceil(m))

            let k = Double(size) / Double(expectedElements) * log(2)
            self.hashCount = Int(ceil(k))

            self.bitArray = Array(repeating: false, count: size)
        }

        /// Add element to filter
        public func add(_ element: String) {
            for i in 0..<hashCount {
                let hash = getHash(element, seed: i)
                bitArray[hash % size] = true
            }
        }

        /// Check if element might be in set
        public func contains(_ element: String) -> Bool {
            for i in 0..<hashCount {
                let hash = getHash(element, seed: i)
                if !bitArray[hash % size] {
                    return false
                }
            }
            return true  // Might be present (or false positive)
        }

        private func getHash(_ string: String, seed: Int) -> Int {
            var hash = seed
            for char in string.unicodeScalars {
                hash = hash &* 31 &+ Int(char.value)
            }
            return abs(hash)
        }
    }

    // MARK: - Skip List

    /// Probabilistic alternative to balanced trees
    public class SkipList<T: Comparable> {
        class Node {
            let value: T?
            var next: [Node?]

            init(value: T?, level: Int) {
                self.value = value
                self.next = Array(repeating: nil, count: level + 1)
            }
        }

        private var head: Node
        private var maxLevel: Int
        private let probability: Double = 0.5

        public init() {
            self.maxLevel = 16
            self.head = Node(value: nil, level: maxLevel)
        }

        private func randomLevel() -> Int {
            var level = 0
            while Double.random(in: 0..<1) < probability && level < maxLevel {
                level += 1
            }
            return level
        }

        /// Insert value into skip list
        public func insert(_ value: T) {
            var update = Array(repeating: head as Node?, count: maxLevel + 1)
            var current: Node? = head

            // Find position to insert
            for i in stride(from: maxLevel, through: 0, by: -1) {
                while let next = current?.next[i],
                      let nextValue = next.value,
                      nextValue < value {
                    current = next
                }
                update[i] = current
            }

            // Insert new node
            let level = randomLevel()
            let newNode = Node(value: value, level: level)

            for i in 0...level {
                newNode.next[i] = update[i]?.next[i]
                update[i]?.next[i] = newNode
            }
        }

        /// Search for value in skip list
        public func search(_ value: T) -> Bool {
            var current: Node? = head

            for i in stride(from: maxLevel, through: 0, by: -1) {
                while let next = current?.next[i],
                      let nextValue = next.value,
                      nextValue < value {
                    current = next
                }
            }

            current = current?.next[0]
            return current?.value == value
        }

        /// Delete value from skip list
        public func delete(_ value: T) -> Bool {
            var update = Array(repeating: head as Node?, count: maxLevel + 1)
            var current: Node? = head

            // Find node to delete
            for i in stride(from: maxLevel, through: 0, by: -1) {
                while let next = current?.next[i],
                      let nextValue = next.value,
                      nextValue < value {
                    current = next
                }
                update[i] = current
            }

            current = current?.next[0]

            if current?.value == value {
                // Remove node
                for i in 0...maxLevel {
                    if update[i]?.next[i] !== current {
                        break
                    }
                    update[i]?.next[i] = current?.next[i]
                }
                return true
            }

            return false
        }
    }

    // MARK: - Reservoir Sampling

    /// Sample k items from a stream of unknown size
    public class ReservoirSampling<T> {
        private var reservoir: [T] = []
        private let k: Int
        private var count = 0

        public init(sampleSize k: Int) {
            self.k = k
        }

        /// Add item to stream
        public func add(_ item: T) {
            count += 1

            if reservoir.count < k {
                reservoir.append(item)
            } else {
                let randomIndex = Int.random(in: 0..<count)
                if randomIndex < k {
                    reservoir[randomIndex] = item
                }
            }
        }

        /// Get current sample
        public var sample: [T] {
            return reservoir
        }

        /// Reset sampling
        public func reset() {
            reservoir.removeAll()
            count = 0
        }
    }
}