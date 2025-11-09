/*
 * QuickSort Algorithm Implementation in Swift
 * 
 * Time Complexity:
 * - Best Case: O(n log n)
 * - Average Case: O(n log n)
 * - Worst Case: O(n²)
 * 
 * Space Complexity: O(log n) due to recursion stack
 * 
 * Swift features:
 * - Protocol-oriented programming
 * - Generic constraints
 * - Functional programming capabilities
 * - Value semantics and copy-on-write
 */

import Foundation

// MARK: - Protocol for Sortable Types
protocol QuickSortable: Comparable {
    // Default implementation will use Comparable
}

extension Int: QuickSortable {}
extension Double: QuickSortable {}
extension String: QuickSortable {}
extension Character: QuickSortable {}

// MARK: - QuickSort Implementation
struct QuickSort {
    
    // MARK: - Public Methods
    
    /// Sorts an array using QuickSort algorithm (returns new array)
    static func sort<T: Comparable>(_ array: [T]) -> [T] {
        guard array.count > 1 else { return array }
        
        var result = array
        sortInPlace(&result, low: 0, high: result.count - 1)
        return result
    }
    
    /// Sorts an array in-place using QuickSort algorithm
    static func sortInPlace<T: Comparable>(_ array: inout [T]) {
        guard array.count > 1 else { return }
        sortInPlace(&array, low: 0, high: array.count - 1)
    }
    
    /// Functional-style QuickSort implementation
    static func sortFunctional<T: Comparable>(_ array: [T]) -> [T] {
        guard array.count > 1 else { return array }
        
        let pivot = array[array.count / 2]
        let less = array.filter { $0 < pivot }
        let equal = array.filter { $0 == pivot }
        let greater = array.filter { $0 > pivot }
        
        return sortFunctional(less) + equal + sortFunctional(greater)
    }
    
    /// Iterative implementation to avoid stack overflow
    static func sortIterative<T: Comparable>(_ array: inout [T]) {
        guard array.count > 1 else { return }
        
        var stack = [(low: Int, high: Int)]()
        stack.append((low: 0, high: array.count - 1))
        
        while !stack.isEmpty {
            let range = stack.removeLast()
            
            if range.low < range.high {
                let pivotIndex = partition(&array, low: range.low, high: range.high)
                stack.append((low: range.low, high: pivotIndex - 1))
                stack.append((low: pivotIndex + 1, high: range.high))
            }
        }
    }
    
    /// Randomized QuickSort for better average performance
    static func sortRandomized<T: Comparable>(_ array: inout [T]) {
        guard array.count > 1 else { return }
        sortRandomizedHelper(&array, low: 0, high: array.count - 1)
    }
    
    /// Three-way partitioning for arrays with many duplicates
    static func sort3Way<T: Comparable>(_ array: inout [T]) {
        guard array.count > 1 else { return }
        sort3WayHelper(&array, low: 0, high: array.count - 1)
    }
    
    /// Sort with custom comparison function
    static func sortBy<T>(_ array: [T], by comparison: @escaping (T, T) -> Bool) -> [T] {
        guard array.count > 1 else { return array }
        
        let pivot = array[array.count / 2]
        let less = array.filter { comparison($0, pivot) }
        let equal = array.filter { !comparison($0, pivot) && !comparison(pivot, $0) }
        let greater = array.filter { comparison(pivot, $0) }
        
        return sortBy(less, by: comparison) + equal + sortBy(greater, by: comparison)
    }
    
    // MARK: - Private Helper Methods
    
    private static func sortInPlace<T: Comparable>(_ array: inout [T], low: Int, high: Int) {
        guard low < high else { return }
        
        let pivotIndex = partition(&array, low: low, high: high)
        sortInPlace(&array, low: low, high: pivotIndex - 1)
        sortInPlace(&array, low: pivotIndex + 1, high: high)
    }
    
    private static func partition<T: Comparable>(_ array: inout [T], low: Int, high: Int) -> Int {
        let pivot = array[high]
        var i = low - 1
        
        for j in low..<high {
            if array[j] <= pivot {
                i += 1
                array.swapAt(i, j)
            }
        }
        
        array.swapAt(i + 1, high)
        return i + 1
    }
    
    private static func sortRandomizedHelper<T: Comparable>(_ array: inout [T], low: Int, high: Int) {
        guard low < high else { return }
        
        // Random pivot selection
        let randomIndex = Int.random(in: low...high)
        array.swapAt(randomIndex, high)
        
        let pivotIndex = partition(&array, low: low, high: high)
        sortRandomizedHelper(&array, low: low, high: pivotIndex - 1)
        sortRandomizedHelper(&array, low: pivotIndex + 1, high: high)
    }
    
    private static func sort3WayHelper<T: Comparable>(_ array: inout [T], low: Int, high: Int) {
        guard low < high else { return }
        
        let pivot = array[low]
        var lt = low
        var gt = high
        var i = low
        
        while i <= gt {
            if array[i] < pivot {
                array.swapAt(lt, i)
                lt += 1
                i += 1
            } else if array[i] > pivot {
                array.swapAt(i, gt)
                gt -= 1
            } else {
                i += 1
            }
        }
        
        sort3WayHelper(&array, low: low, high: lt - 1)
        sort3WayHelper(&array, low: gt + 1, high: high)
    }
}

// MARK: - Array Extensions
extension Array where Element: Comparable {
    /// Quick sort the array and return a new sorted array
    func quickSorted() -> [Element] {
        return QuickSort.sort(self)
    }
    
    /// Sort the array in-place using QuickSort
    mutating func quickSort() {
        QuickSort.sortInPlace(&self)
    }
    
    /// Check if array is sorted
    var isSorted: Bool {
        guard count > 1 else { return true }
        return zip(self, self.dropFirst()).allSatisfy(<=)
    }
    
    /// Quick sort using functional approach
    func quickSortedFunctional() -> [Element] {
        return QuickSort.sortFunctional(self)
    }
    
    /// Quick sort with 3-way partitioning
    mutating func quickSort3Way() {
        QuickSort.sort3Way(&self)
    }
}

// MARK: - Performance Benchmark
struct QuickSortBenchmark {
    
    static func run() {
        print("🚀 Swift QuickSort Performance Benchmark")
        print(String(repeating: "=", count: 40))
        
        let sizes = [1_000, 10_000, 100_000]
        
        for size in sizes {
            print("\nTesting with \(size.formatted()) elements:")
            
            let testData = generateRandomArray(size: size, range: 1...1000)
            
            benchmarkImplementation("Standard", data: testData) { array in
                var mutableArray = array
                QuickSort.sortInPlace(&mutableArray)
                return mutableArray
            }
            
            benchmarkImplementation("Functional", data: testData) { array in
                return QuickSort.sortFunctional(array)
            }
            
            benchmarkImplementation("Iterative", data: testData) { array in
                var mutableArray = array
                QuickSort.sortIterative(&mutableArray)
                return mutableArray
            }
            
            benchmarkImplementation("Randomized", data: testData) { array in
                var mutableArray = array
                QuickSort.sortRandomized(&mutableArray)
                return mutableArray
            }
            
            benchmarkImplementation("3-Way", data: testData) { array in
                var mutableArray = array
                QuickSort.sort3Way(&mutableArray)
                return mutableArray
            }
        }
    }
    
    private static func generateRandomArray(size: Int, range: ClosedRange<Int>) -> [Int] {
        return (0..<size).map { _ in Int.random(in: range) }
    }
    
    private static func benchmarkImplementation(_ name: String, 
                                              data: [Int], 
                                              implementation: ([Int]) -> [Int]) {
        let startTime = CFAbsoluteTimeGetCurrent()
        let result = implementation(data)
        let timeElapsed = CFAbsoluteTimeGetCurrent() - startTime
        
        let isCorrect = result.isSorted
        print("  \(name.padding(toLength: 12, withPad: " ", startingAt: 0)): \(String(format: "%.3f", timeElapsed * 1000)) ms \(isCorrect ? "✓" : "✗")")
    }
}

// MARK: - Demo and Testing
class QuickSortDemo {
    
    static func run() {
        print("🚀 Swift QuickSort Implementation")
        print(String(repeating: "=", count: 40))
        
        testBasicSorting()
        testAdvancedFeatures()
        QuickSortBenchmark.run()
        
        print("\n✨ QuickSort demonstration complete!")
    }
    
    private static func testBasicSorting() {
        print("\n📋 Basic Sorting Tests")
        print(String(repeating: "-", count: 30))
        
        let testArrays: [[Int]] = [
            [64, 34, 25, 12, 22, 11, 90],
            [5, 2, 8, 6, 1, 9, 4],
            [1],
            [],
            [3, 3, 3, 3, 3],
            [9, 8, 7, 6, 5, 4, 3, 2, 1]
        ]
        
        for (index, array) in testArrays.enumerated() {
            let sorted = QuickSort.sort(array)
            
            print("\nTest \(index + 1):")
            print("Original: \(array)")
            print("Sorted:   \(sorted)")
            print("Correct:  \(sorted.isSorted)")
        }
    }
    
    private static func testAdvancedFeatures() {
        print("\n🎯 Advanced Features")
        print(String(repeating: "-", count: 25))
        
        // Test with strings
        let words = ["banana", "apple", "cherry", "date", "elderberry"]
        let sortedWords = QuickSort.sort(words)
        print("\nString sorting:")
        print("Original: \(words)")
        print("Sorted:   \(sortedWords)")
        
        // Test with custom comparison
        let numbers = [64, 34, 25, 12, 22, 11, 90]
        let reverseSorted = QuickSort.sortBy(numbers) { $0 > $1 }
        print("\nReverse sorting:")
        print("Original: \(numbers)")
        print("Reverse:  \(reverseSorted)")
        
        // Test functional approach
        let functionalSorted = QuickSort.sortFunctional(numbers)
        print("\nFunctional approach:")
        print("Original:   \(numbers)")
        print("Functional: \(functionalSorted)")
        
        // Test array extensions
        var extArray = [9, 3, 7, 1, 5]
        print("\nArray extensions:")
        print("Original: \(extArray)")
        
        let newSorted = extArray.quickSorted()
        print("New copy: \(newSorted)")
        
        extArray.quickSort()
        print("In-place: \(extArray)")
        
        // Test with custom types
        struct Person: Comparable {
            let name: String
            let age: Int
            
            static func < (lhs: Person, rhs: Person) -> Bool {
                return lhs.age < rhs.age
            }
            
            static func == (lhs: Person, rhs: Person) -> Bool {
                return lhs.age == rhs.age && lhs.name == rhs.name
            }
        }
        
        let people = [
            Person(name: "Alice", age: 30),
            Person(name: "Bob", age: 25),
            Person(name: "Charlie", age: 35)
        ]
        
        let sortedPeople = QuickSort.sort(people)
        print("\nCustom type sorting (by age):")
        people.forEach { print("  \($0.name): \($0.age)") }
        print("Sorted:")
        sortedPeople.forEach { print("  \($0.name): \($0.age)") }
        
        // Sort by name using custom comparison
        let sortedByName = QuickSort.sortBy(people) { $0.name < $1.name }
        print("\nSorted by name:")
        sortedByName.forEach { print("  \($0.name): \($0.age)") }
    }
}

// MARK: - Main Execution
if CommandLine.argc > 0 && CommandLine.arguments[0].contains("quicksort.swift") {
    QuickSortDemo.run()
}

// MARK: - Unit Tests (for Xcode projects)
#if DEBUG
import XCTest

class QuickSortTests: XCTestCase {
    
    func testEmptyArray() {
        let array: [Int] = []
        let sorted = QuickSort.sort(array)
        XCTAssertEqual(sorted, [])
    }
    
    func testSingleElement() {
        let array = [42]
        let sorted = QuickSort.sort(array)
        XCTAssertEqual(sorted, [42])
    }
    
    func testAlreadySorted() {
        let array = [1, 2, 3, 4, 5]
        let sorted = QuickSort.sort(array)
        XCTAssertEqual(sorted, [1, 2, 3, 4, 5])
    }
    
    func testReverseSorted() {
        let array = [5, 4, 3, 2, 1]
        let sorted = QuickSort.sort(array)
        XCTAssertEqual(sorted, [1, 2, 3, 4, 5])
    }
    
    func testDuplicates() {
        let array = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        let sorted = QuickSort.sort(array)
        XCTAssertEqual(sorted, [1, 1, 2, 3, 4, 5, 5, 6, 9])
    }
    
    func testFunctionalApproach() {
        let array = [64, 34, 25, 12, 22, 11, 90]
        let sorted = QuickSort.sortFunctional(array)
        XCTAssertEqual(sorted, [11, 12, 22, 25, 34, 64, 90])
    }
    
    func testStringsSorting() {
        let array = ["banana", "apple", "cherry"]
        let sorted = QuickSort.sort(array)
        XCTAssertEqual(sorted, ["apple", "banana", "cherry"])
    }
    
    func testPerformanceStandard() {
        let array = Array(0..<10000).shuffled()
        measure {
            var mutableArray = array
            QuickSort.sortInPlace(&mutableArray)
        }
    }
    
    func testPerformanceFunctional() {
        let array = Array(0..<1000).shuffled()
        measure {
            _ = QuickSort.sortFunctional(array)
        }
    }
}
#endif
