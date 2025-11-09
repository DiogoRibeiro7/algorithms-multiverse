# Insertion Sort Algorithm Implementation in Ruby
#
# Time Complexity:
# - Best Case: O(n) - when array is already sorted
# - Average Case: O(n²)
# - Worst Case: O(n²) - when array is reverse sorted
# Space Complexity: O(1) for in-place, O(n) for functional approach
#
# Insertion Sort builds the final sorted array one item at a time.
#
# Ruby features:
# - Idiomatic Ruby method naming (snake_case)
# - Module organization
# - Blocks and lambdas for custom comparators
# - Mixins for extension methods
# - Symbols and hash-based options

module AlgorithmsMultiverse
  module Sorting
    # MARK: - Basic Insertion Sort

    # Performs standard insertion sort.
    #
    # Time Complexity: O(n²) average and worst case, O(n) best case
    # Space Complexity: O(n) for the new array
    #
    # Example visualization:
    #   Initial: [5, 2, 8, 6, 1]
    #   Step 1:  [2, 5, 8, 6, 1]  # Insert 2
    #   Step 2:  [2, 5, 8, 6, 1]  # 8 already in place
    #   Step 3:  [2, 5, 6, 8, 1]  # Insert 6
    #   Step 4:  [1, 2, 5, 6, 8]  # Insert 1
    #
    # @param arr [Array] The array to sort
    # @param comparator [Proc, nil] Optional comparison block/proc
    # @return [Array] A new sorted array
    def self.insertion_sort(arr, &comparator)
      return arr.dup if arr.length <= 1

      result = arr.dup
      insertion_sort_in_place!(result, &comparator)
      result
    end

    # Sorts the array in-place using insertion sort.
    #
    # Time Complexity: O(n²) average and worst case, O(n) best case
    # Space Complexity: O(1)
    #
    # @param arr [Array] The array to sort (modified in-place)
    # @param comparator [Proc, nil] Optional comparison block/proc
    # @return [Array] The sorted array
    def self.insertion_sort_in_place!(arr, &comparator)
      comparator ||= ->(a, b) { a <=> b }

      (1...arr.length).each do |i|
        key = arr[i]
        j = i - 1

        # Move elements greater than key one position ahead
        while j >= 0 && comparator.call(arr[j], key) > 0
          arr[j + 1] = arr[j]
          j -= 1
        end

        arr[j + 1] = key
      end

      arr
    end

    # MARK: - Recursive Insertion Sort

    # Performs recursive insertion sort.
    #
    # Time Complexity: O(n²)
    # Space Complexity: O(n) for recursion stack
    #
    # @param arr [Array] The array to sort
    # @return [Array] A new sorted array
    def self.insertion_sort_recursive(arr)
      return arr.dup if arr.length <= 1

      result = arr.dup
      insertion_sort_recursive_helper!(result, result.length)
      result
    end

    # Helper function for recursive insertion sort.
    #
    # @param arr [Array] The array to sort
    # @param n [Integer] The number of elements to sort
    def self.insertion_sort_recursive_helper!(arr, n)
      # Base case
      return if n <= 1

      # Sort first n-1 elements
      insertion_sort_recursive_helper!(arr, n - 1)

      # Insert last element at its correct position
      key = arr[n - 1]
      j = n - 2

      while j >= 0 && arr[j] > key
        arr[j + 1] = arr[j]
        j -= 1
      end

      arr[j + 1] = key
    end

    # MARK: - Binary Insertion Sort

    # Uses binary search to find insertion position.
    #
    # Time Complexity: O(n²) for moves, O(n log n) for comparisons
    # Space Complexity: O(n)
    #
    # @param arr [Array] The array to sort
    # @return [Array] A new sorted array
    def self.binary_insertion_sort(arr)
      return arr.dup if arr.length <= 1

      result = arr.dup

      (1...result.length).each do |i|
        key = result[i]

        # Find position using binary search
        pos = binary_search_position(result, 0, i - 1, key)

        # Shift elements to make space
        (i - 1).downto(pos) do |j|
          result[j + 1] = result[j]
        end

        result[pos] = key
      end

      result
    end

    # Binary search to find the correct insertion position.
    #
    # @param arr [Array] The array
    # @param left [Integer] Left boundary
    # @param right [Integer] Right boundary
    # @param key The key to insert
    # @return [Integer] The position to insert
    def self.binary_search_position(arr, left, right, key)
      return (key > arr[left] ? left + 1 : left) if right <= left

      mid = (left + right) / 2

      return mid + 1 if key == arr[mid]

      if key > arr[mid]
        binary_search_position(arr, mid + 1, right, key)
      else
        binary_search_position(arr, left, mid - 1, key)
      end
    end

    # MARK: - Shell Sort

    # Performs shell sort (generalization of insertion sort).
    #
    # Time Complexity: Depends on gap sequence (O(n log²n) for good sequences)
    # Space Complexity: O(n)
    #
    # @param arr [Array] The array to sort
    # @return [Array] A new sorted array
    def self.shell_sort(arr)
      return arr.dup if arr.length <= 1

      result = arr.dup
      n = result.length

      # Start with a large gap, then reduce (Knuth's sequence)
      gap = 1
      gap = 3 * gap + 1 while gap < n / 3

      # Perform gapped insertion sort
      while gap > 0
        (gap...n).each do |i|
          key = result[i]
          j = i

          # Insertion sort with gap
          while j >= gap && result[j - gap] > key
            result[j] = result[j - gap]
            j -= gap
          end

          result[j] = key
        end

        gap /= 3
      end

      result
    end

    # MARK: - Sort Statistics

    # Tracks sorting operations
    class SortStatistics
      attr_accessor :comparisons, :swaps

      def initialize
        @comparisons = 0
        @swaps = 0
      end

      def reset
        @comparisons = 0
        @swaps = 0
      end

      def to_s
        "Comparisons: #{@comparisons}, Swaps: #{@swaps}"
      end
    end

    # Insertion sort with statistics tracking
    #
    # @param arr [Array] The array to sort
    # @param stats [SortStatistics] Statistics object to track operations
    # @return [Array] A new sorted array
    def self.insertion_sort_with_stats(arr, stats)
      stats.reset
      return arr.dup if arr.length <= 1

      result = arr.dup

      (1...result.length).each do |i|
        key = result[i]
        j = i - 1

        while j >= 0
          stats.comparisons += 1
          if result[j] > key
            result[j + 1] = result[j]
            stats.swaps += 1
            j -= 1
          else
            break
          end
        end

        result[j + 1] = key
      end

      result
    end

    # MARK: - Visualization

    # Creates a step-by-step visualization of insertion sort
    #
    # @param arr [Array<Integer>] The array to visualize
    # @return [Array<String>] Array of strings showing each step
    def self.visualize_insertion_sort(arr)
      steps = []
      result = arr.dup

      steps << "Initial: #{result}"

      (1...result.length).each do |i|
        key = result[i]
        j = i - 1

        steps << "\nStep #{i}: Inserting #{key}"
        steps << "  Before: #{result}"

        while j >= 0 && result[j] > key
          result[j + 1] = result[j]
          j -= 1
        end

        result[j + 1] = key
        steps << "  After:  #{result}"
      end

      steps << "\nFinal: #{result}"
      steps
    end

    # MARK: - Stability Demonstration

    # Demonstrates that insertion sort is stable
    def self.demonstrate_stability
      Pair = Struct.new(:value, :original_index)

      data = [
        Pair.new(3, 0),
        Pair.new(1, 1),
        Pair.new(3, 2),
        Pair.new(2, 3),
        Pair.new(3, 4)
      ]

      # Sort by value only
      sorted = insertion_sort(data) { |a, b| a.value <=> b.value }

      puts "Stability Demonstration:"
      print "Original: "
      data.each { |p| print "(#{p.value},#{p.original_index}) " }
      puts

      print "Sorted:   "
      sorted.each { |p| print "(#{p.value},#{p.original_index}) " }
      puts

      # Check stability - all 3's should maintain original order
      three_indices = sorted.select { |p| p.value == 3 }.map(&:original_index)
      is_stable = three_indices == [0, 2, 4]
      puts "Stable: #{is_stable} (indices of 3's: #{three_indices})"
    end

    # MARK: - Helper Functions

    # Check if an array is sorted in ascending order
    #
    # @param arr [Array] The array to check
    # @return [Boolean] True if sorted, false otherwise
    def self.sorted?(arr)
      (0...arr.length - 1).all? { |i| arr[i] <= arr[i + 1] }
    end
  end
end

# MARK: - Array Extension

class Array
  # Returns a new array sorted using insertion sort
  #
  # @param comparator [Proc, nil] Optional comparison block
  # @return [Array] A new sorted array
  def insertion_sorted(&comparator)
    AlgorithmsMultiverse::Sorting.insertion_sort(self, &comparator)
  end

  # Sorts the array in-place using insertion sort
  #
  # @param comparator [Proc, nil] Optional comparison block
  # @return [Array] Self
  def insertion_sort!(&comparator)
    AlgorithmsMultiverse::Sorting.insertion_sort_in_place!(self, &comparator)
  end

  # Check if array is sorted
  #
  # @return [Boolean] True if sorted
  def sorted?
    AlgorithmsMultiverse::Sorting.sorted?(self)
  end
end

# MARK: - Demonstration and Testing

def demonstrate_insertion_sort
  include AlgorithmsMultiverse::Sorting

  puts "📝 Insertion Sort Implementation in Ruby"
  puts "=" * 60

  # Test data
  test_cases = [
    { arr: [64, 34, 25, 12, 22, 11, 90], desc: "Random array" },
    { arr: [5, 2, 8, 6, 1, 9, 4], desc: "Small random array" },
    { arr: [1], desc: "Single element" },
    { arr: [], desc: "Empty array" },
    { arr: [3, 3, 3, 3, 3], desc: "All duplicates" },
    { arr: [9, 8, 7, 6, 5, 4, 3, 2, 1], desc: "Reverse sorted" },
    { arr: [1, 2, 3, 4, 5], desc: "Already sorted" },
    { arr: [1, 3, 2, 4, 5], desc: "Nearly sorted" }
  ]

  puts "\n📋 Basic Sorting Tests:"
  puts "-" * 60

  test_cases.each do |tc|
    standard_result = AlgorithmsMultiverse::Sorting.insertion_sort(tc[:arr])
    binary_result = AlgorithmsMultiverse::Sorting.binary_insertion_sort(tc[:arr])
    shell_result = AlgorithmsMultiverse::Sorting.shell_sort(tc[:arr])
    recursive_result = AlgorithmsMultiverse::Sorting.insertion_sort_recursive(tc[:arr])

    puts "\nTest: #{tc[:desc]}"
    puts "Original: #{tc[:arr]}"
    puts "Sorted:   #{standard_result}"

    all_correct = standard_result.sorted? && binary_result.sorted? &&
                 shell_result.sorted? && recursive_result.sorted?
    all_equal = (standard_result == binary_result) &&
               (standard_result == shell_result) &&
               (standard_result == recursive_result)

    status = (all_correct && all_equal) ? "✓" : "✗"
    puts "All implementations match: #{status}"
  end

  # Visualization demo
  puts "\n\n🎬 Step-by-Step Visualization:"
  puts "-" * 60

  demo_arr = [5, 2, 8, 6, 1]
  steps = AlgorithmsMultiverse::Sorting.visualize_insertion_sort(demo_arr)
  steps.each { |step| puts step }

  # Stability demonstration
  puts "\n\n🔒 Stability Demonstration:"
  puts "-" * 60
  AlgorithmsMultiverse::Sorting.demonstrate_stability

  # Performance analysis
  puts "\n\n📊 Operation Counting:"
  puts "-" * 60

  stat_test_cases = [
    { arr: [5, 2, 8, 6, 1], desc: "Random" },
    { arr: [1, 2, 3, 4, 5], desc: "Already sorted" },
    { arr: [5, 4, 3, 2, 1], desc: "Reverse sorted" }
  ]

  stat_test_cases.each do |tc|
    stats = AlgorithmsMultiverse::Sorting::SortStatistics.new
    AlgorithmsMultiverse::Sorting.insertion_sort_with_stats(tc[:arr], stats)

    n = tc[:arr].length
    puts "\n#{tc[:desc]}: #{tc[:arr]}"
    puts "Array size (n): #{n}"
    puts "Comparisons: #{stats.comparisons}"
    puts "Swaps: #{stats.swaps}"
    puts "Best case comparisons: #{n - 1}"
    puts "Worst case comparisons: #{n * (n - 1) / 2}"
  end
end

# MARK: - Performance Benchmark

def performance_benchmark
  require 'benchmark'
  include AlgorithmsMultiverse::Sorting

  puts "\n\n⚡ Performance Benchmark"
  puts "=" * 80
  puts "\nInsertion sort is preferred for:"
  puts "  • Small arrays (typically n < 10-20)"
  puts "  • Nearly sorted arrays"
  puts "  • As part of hybrid sorting algorithms"
  puts

  sizes = [5, 10, 20, 50, 100, 500, 1000]

  patterns = {
    'Random' => ->(n) { Array.new(n) { rand(1..1000) } },
    'Nearly Sorted' => lambda { |n|
      arr = (0...n).to_a
      [5, n / 10].min.times do
        idx1, idx2 = rand(n), rand(n)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
      end
      arr
    },
    'Reversed' => ->(n) { (0...n).to_a.reverse }
  }

  patterns.each do |pattern_name, pattern_gen|
    puts "\n#{pattern_name} Data:"
    puts format("%-8s%15s%15s%15s%15s", "Size", "Insertion", "Binary", "Shell", "sort()")
    puts "-" * 68

    sizes.each do |size|
      test_data = pattern_gen.call(size)
      print format("%-8d", size)

      # Insertion Sort
      elapsed = Benchmark.measure {
        AlgorithmsMultiverse::Sorting.insertion_sort(test_data)
      }.real * 1000
      print format("%14.3fms", elapsed)

      # Binary Insertion Sort
      elapsed = Benchmark.measure {
        AlgorithmsMultiverse::Sorting.binary_insertion_sort(test_data)
      }.real * 1000
      print format("%14.3fms", elapsed)

      # Shell Sort
      elapsed = Benchmark.measure {
        AlgorithmsMultiverse::Sorting.shell_sort(test_data)
      }.real * 1000
      print format("%14.3fms", elapsed)

      # Ruby sort()
      elapsed = Benchmark.measure {
        test_data.sort
      }.real * 1000
      puts format("%14.3fms", elapsed)
    end
  end
end

# MARK: - Main

if __FILE__ == $PROGRAM_NAME
  demonstrate_insertion_sort
  performance_benchmark

  puts "\n✨ Insertion Sort demonstration complete!"
end
