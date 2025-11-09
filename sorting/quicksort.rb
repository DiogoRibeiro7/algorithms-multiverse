# QuickSort Algorithm Implementation in Ruby
# 
# Time Complexity:
# - Best Case: O(n log n)
# - Average Case: O(n log n)  
# - Worst Case: O(n²)
# 
# Space Complexity: O(log n) due to recursion stack
# 
# Ruby features:
# - Duck typing
# - Elegant block syntax
# - Functional programming style

class QuickSort
  # Main sorting method - returns new sorted array
  def self.sort(array)
    return array if array.length <= 1
    
    pivot = array.sample
    less_than_pivot = array.select { |x| x < pivot }
    equal_to_pivot = array.select { |x| x == pivot }
    greater_than_pivot = array.select { |x| x > pivot }
    
    sort(less_than_pivot) + equal_to_pivot + sort(greater_than_pivot)
  end
  
  # In-place sorting method
  def self.sort!(array)
    sort_in_place!(array, 0, array.length - 1)
    array
  end
  
  # Recursive in-place helper method
  def self.sort_in_place!(array, low, high)
    return if low >= high
    
    pivot_index = partition!(array, low, high)
    sort_in_place!(array, low, pivot_index - 1)
    sort_in_place!(array, pivot_index + 1, high)
  end
  
  # Partition method for in-place sorting
  def self.partition!(array, low, high)
    pivot = array[high]
    i = low
    
    (low...high).each do |j|
      if array[j] <= pivot
        array[i], array[j] = array[j], array[i]
        i += 1
      end
    end
    
    array[i], array[high] = array[high], array[i]
    i
  end
  
  # Iterative implementation to avoid recursion overhead
  def self.sort_iterative!(array)
    return array if array.length <= 1
    
    stack = [[0, array.length - 1]]
    
    until stack.empty?
      low, high = stack.pop
      
      if low < high
        pivot_index = partition!(array, low, high)
        stack.push([low, pivot_index - 1]) if pivot_index > 0
        stack.push([pivot_index + 1, high])
      end
    end
    
    array
  end
  
  # Randomized pivot selection for better performance
  def self.randomized_sort!(array, low = 0, high = array.length - 1)
    return if low >= high
    
    # Random pivot selection
    random_index = rand(low..high)
    array[random_index], array[high] = array[high], array[random_index]
    
    pivot_index = partition!(array, low, high)
    randomized_sort!(array, low, pivot_index - 1)
    randomized_sort!(array, pivot_index + 1, high)
  end
  
  # Three-way partitioning for arrays with many duplicates
  def self.sort_3way!(array, low = 0, high = array.length - 1)
    return if low >= high
    
    pivot = array[low]
    lt = low
    gt = high
    i = low
    
    while i <= gt
      if array[i] < pivot
        array[lt], array[i] = array[i], array[lt]
        lt += 1
        i += 1
      elsif array[i] > pivot
        array[i], array[gt] = array[gt], array[i]
        gt -= 1
      else
        i += 1
      end
    end
    
    sort_3way!(array, low, lt - 1) if lt > 0
    sort_3way!(array, gt + 1, high)
  end
  
  # Sort with custom comparison block
  def self.sort_by(array, &comparator)
    return array if array.length <= 1
    
    pivot = array[array.length / 2]
    less_than_pivot = array.select { |x| comparator.call(x, pivot) < 0 }
    equal_to_pivot = array.select { |x| comparator.call(x, pivot) == 0 }
    greater_than_pivot = array.select { |x| comparator.call(x, pivot) > 0 }
    
    sort_by(less_than_pivot, &comparator) + 
    equal_to_pivot + 
    sort_by(greater_than_pivot, &comparator)
  end
end

# Module for additional utility methods
module QuickSortUtils
  # Benchmark sorting performance
  def self.benchmark(array, iterations = 1)
    total_time = 0
    
    iterations.times do
      test_array = array.dup
      start_time = Time.now
      QuickSort.sort!(test_array)
      total_time += (Time.now - start_time)
    end
    
    average_time = total_time / iterations
    puts "Average time for #{array.length} elements: #{average_time.round(6)}s"
    average_time
  end
  
  # Verify if array is sorted
  def self.sorted?(array)
    (0...array.length - 1).all? { |i| array[i] <= array[i + 1] }
  end
  
  # Generate test data
  def self.generate_test_data(size, range = 1..1000)
    Array.new(size) { rand(range) }
  end
end

# Extended Array class with QuickSort methods
class Array
  def quicksort
    QuickSort.sort(self)
  end
  
  def quicksort!
    QuickSort.sort!(self)
  end
  
  def quicksort_3way!
    QuickSort.sort_3way!(self)
    self
  end
end

# Example usage and testing
if __FILE__ == $0
  puts "🚀 Ruby QuickSort Implementation"
  puts "=" * 40
  
  # Test data
  test_arrays = [
    [64, 34, 25, 12, 22, 11, 90],
    [5, 2, 8, 6, 1, 9, 4],
    [1],
    [],
    [3, 3, 3, 3, 3],
    [9, 8, 7, 6, 5, 4, 3, 2, 1],
    %w[ruby python java javascript go rust]
  ]
  
  # Test all implementations
  test_arrays.each_with_index do |arr, index|
    puts "\nTest #{index + 1}:"
    puts "Original: #{arr.inspect}"
    
    # Test functional approach
    sorted = QuickSort.sort(arr.dup)
    puts "Sorted:   #{sorted.inspect}"
    puts "Correct:  #{QuickSortUtils.sorted?(sorted)}"
  end
  
  # Performance testing
  puts "\n📊 Performance Testing"
  puts "=" * 30
  
  sizes = [1000, 10000, 50000]
  sizes.each do |size|
    puts "\nTesting with #{size} elements:"
    test_data = QuickSortUtils.generate_test_data(size)
    
    # Test different implementations
    puts "Functional approach:"
    QuickSortUtils.benchmark(test_data)
    
    puts "In-place approach:"
    test_copy = test_data.dup
    start_time = Time.now
    QuickSort.sort!(test_copy)
    puts "Time: #{(Time.now - start_time).round(6)}s"
    
    puts "3-way partitioning:"
    test_copy = test_data.dup
    start_time = Time.now
    QuickSort.sort_3way!(test_copy)
    puts "Time: #{(Time.now - start_time).round(6)}s"
  end
  
  # Demonstration of advanced features
  puts "\n🎯 Advanced Features"
  puts "=" * 25
  
  # Custom sorting with blocks
  people = [
    { name: "Alice", age: 30 },
    { name: "Bob", age: 25 },
    { name: "Charlie", age: 35 }
  ]
  
  puts "Original people: #{people.inspect}"
  
  # Sort by age
  sorted_by_age = QuickSort.sort_by(people) { |a, b| a[:age] <=> b[:age] }
  puts "Sorted by age: #{sorted_by_age.inspect}"
  
  # Sort by name
  sorted_by_name = QuickSort.sort_by(people) { |a, b| a[:name] <=> b[:name] }
  puts "Sorted by name: #{sorted_by_name.inspect}"
  
  # Reverse sorting
  numbers = [1, 5, 3, 9, 2, 8, 4]
  puts "\nOriginal numbers: #{numbers}"
  
  reverse_sorted = QuickSort.sort_by(numbers) { |a, b| b <=> a }
  puts "Reverse sorted: #{reverse_sorted}"
  
  # Using Array extensions
  puts "\nUsing Array extensions:"
  test_array = [64, 34, 25, 12, 22, 11, 90]
  puts "Original: #{test_array}"
  puts "Sorted:   #{test_array.quicksort}"
  
  puts "\n✨ QuickSort demonstration complete!"
end
