# Comprehensive Linked List Implementations in Ruby
#
# Features:
# - Dynamic typing with duck typing
# - Block/Proc support for callbacks
# - All 4 variants: Singly, Doubly, Circular, Skip List
# - Enumerable module inclusion
#
# Usage:
#   ruby linkedlist.rb

# ============================================================================
# SINGLY LINKED LIST
# ============================================================================

class SinglyNode
  attr_accessor :data, :next

  def initialize(data)
    @data = data
    @next = nil
  end
end

class SinglyLinkedList
  include Enumerable

  attr_reader :size

  def initialize
    @head = nil
    @size = 0
  end

  def insert_at_head(data)
    new_node = SinglyNode.new(data)
    new_node.next = @head
    @head = new_node
    @size += 1
  end

  def insert_at_tail(data)
    new_node = SinglyNode.new(data)

    if @head.nil?
      @head = new_node
    else
      current = @head
      current = current.next while current.next
      current.next = new_node
    end

    @size += 1
  end

  def delete_at_head
    return nil if @head.nil?

    data = @head.data
    @head = @head.next
    @size -= 1
    data
  end

  def search(value = nil, &block)
    current = @head

    while current
      if block_given?
        return current.data if yield(current.data)
      else
        return current.data if current.data == value
      end
      current = current.next
    end

    nil
  end

  def reverse!
    prev = nil
    current = @head

    while current
      next_node = current.next
      current.next = prev
      prev = current
      current = next_node
    end

    @head = prev
    self
  end

  def get_middle
    return nil if @head.nil?

    slow = @head
    fast = @head

    while fast.next && fast.next.next
      slow = slow.next
      fast = fast.next.next
    end

    slow.data
  end

  def detect_cycle?
    return false if @head.nil?

    slow = @head
    fast = @head

    while fast && fast.next
      slow = slow.next
      fast = fast.next.next
      return true if slow == fast
    end

    false
  end

  # Enumerable support
  def each
    return enum_for(:each) unless block_given?

    current = @head
    while current
      yield current.data
      current = current.next
    end
  end

  def empty?
    @head.nil?
  end

  def to_s
    map(&:to_s).join(' -> ') + ' -> nil'
  end

  alias_method :inspect, :to_s
end

# ============================================================================
# DOUBLY LINKED LIST
# ============================================================================

class DoublyNode
  attr_accessor :data, :next, :prev

  def initialize(data)
    @data = data
    @next = nil
    @prev = nil
  end
end

class DoublyLinkedList
  include Enumerable

  attr_reader :size

  def initialize
    @head = nil
    @tail = nil
    @size = 0
  end

  def insert_at_head(data)
    new_node = DoublyNode.new(data)

    if @head.nil?
      @head = @tail = new_node
    else
      new_node.next = @head
      @head.prev = new_node
      @head = new_node
    end

    @size += 1
  end

  def insert_at_tail(data)
    new_node = DoublyNode.new(data)

    if @tail.nil?
      @head = @tail = new_node
    else
      new_node.prev = @tail
      @tail.next = new_node
      @tail = new_node
    end

    @size += 1
  end

  def delete_at_head
    return nil if @head.nil?

    data = @head.data

    if @head == @tail
      @head = @tail = nil
    else
      @head = @head.next
      @head.prev = nil
    end

    @size -= 1
    data
  end

  def delete_at_tail
    return nil if @tail.nil?

    data = @tail.data

    if @head == @tail
      @head = @tail = nil
    else
      @tail = @tail.prev
      @tail.next = nil
    end

    @size -= 1
    data
  end

  def reverse!
    current = @head
    @head, @tail = @tail, @head

    while current
      current.prev, current.next = current.next, current.prev
      current = current.prev
    end

    self
  end

  # Forward iteration (default)
  def each
    return enum_for(:each) unless block_given?

    current = @head
    while current
      yield current.data
      current = current.next
    end
  end

  # Backward iteration
  def reverse_each
    return enum_for(:reverse_each) unless block_given?

    current = @tail
    while current
      yield current.data
      current = current.prev
    end
  end

  def empty?
    @head.nil?
  end

  def to_s
    map(&:to_s).join(' <-> ') + ' <-> nil'
  end

  alias_method :inspect, :to_s
end

# ============================================================================
# CIRCULAR LINKED LIST
# ============================================================================

class CircularLinkedList
  attr_reader :size

  def initialize
    @head = nil
    @size = 0
  end

  def insert_at_tail(data)
    new_node = SinglyNode.new(data)

    if @head.nil?
      new_node.next = new_node
      @head = new_node
    else
      current = @head
      current = current.next while current.next != @head

      current.next = new_node
      new_node.next = @head
    end

    @size += 1
  end

  def delete_at_head
    return nil if @head.nil?

    data = @head.data

    if @head.next == @head
      @head = nil
    else
      current = @head
      current = current.next while current.next != @head

      current.next = @head.next
      @head = @head.next
    end

    @size -= 1
    data
  end

  def each
    return enum_for(:each) unless block_given?
    return if @head.nil?

    current = @head
    loop do
      yield current.data
      current = current.next
      break if current == @head
    end
  end

  def empty?
    @head.nil?
  end

  def to_s
    return 'Empty' if @head.nil?

    elements = []
    current = @head

    loop do
      elements << current.data.to_s
      current = current.next
      break if current == @head
    end

    elements.join(' -> ') + ' -> (head)'
  end

  alias_method :inspect, :to_s
end

# ============================================================================
# SKIP LIST
# ============================================================================

class SkipNode
  attr_accessor :data, :forward

  def initialize(data, level)
    @data = data
    @forward = Array.new(level + 1)
  end
end

class SkipList
  MAX_LEVEL = 16
  P = 0.5

  attr_reader :size

  def initialize
    @header = SkipNode.new(nil, MAX_LEVEL)
    @level = 0
    @size = 0
  end

  def random_level
    lvl = 0
    lvl += 1 while rand < P && lvl < MAX_LEVEL
    lvl
  end

  def insert(data)
    update = Array.new(MAX_LEVEL + 1)
    current = @header

    @level.downto(0) do |i|
      while current.forward[i] && current.forward[i].data < data
        current = current.forward[i]
      end
      update[i] = current
    end

    new_level = random_level

    if new_level > @level
      ((@level + 1)..new_level).each do |i|
        update[i] = @header
      end
      @level = new_level
    end

    new_node = SkipNode.new(data, new_level)

    (0..new_level).each do |i|
      new_node.forward[i] = update[i].forward[i]
      update[i].forward[i] = new_node
    end

    @size += 1
  end

  def search(data)
    current = @header

    @level.downto(0) do |i|
      while current.forward[i] && current.forward[i].data < data
        current = current.forward[i]
      end
    end

    current = current.forward[0]
    current && current.data == data
  end

  def delete(data)
    update = Array.new(MAX_LEVEL + 1)
    current = @header

    @level.downto(0) do |i|
      while current.forward[i] && current.forward[i].data < data
        current = current.forward[i]
      end
      update[i] = current
    end

    current = current.forward[0]

    return false unless current && current.data == data

    (0..@level).each do |i|
      break if update[i].forward[i] != current
      update[i].forward[i] = current.forward[i]
    end

    @level -= 1 while @level > 0 && @header.forward[@level].nil?

    @size -= 1
    true
  end

  def to_a
    result = []
    current = @header.forward[0]

    while current
      result << current.data
      current = current.forward[0]
    end

    result
  end

  def to_s
    "SkipList#{to_a}"
  end

  alias_method :inspect, :to_s
end

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate
  puts '=' * 80
  puts 'COMPREHENSIVE LINKED LIST DEMONSTRATIONS IN RUBY'
  puts '=' * 80

  # Singly Linked List
  puts "\n1. SINGLY LINKED LIST"
  puts '-' * 80
  sll = SinglyLinkedList.new

  puts 'Inserting: 1, 2, 3 at head'
  sll.insert_at_head(3)
  sll.insert_at_head(2)
  sll.insert_at_head(1)
  puts "List: #{sll}"

  puts "\nInserting: 4, 5 at tail"
  sll.insert_at_tail(4)
  sll.insert_at_tail(5)
  puts "List: #{sll}"

  puts "\nMiddle element: #{sll.get_middle}"

  puts "\nReversing list..."
  sll.reverse!
  puts "List: #{sll}"

  puts "\nUsing blocks - find first even number:"
  even = sll.search { |x| x.even? }
  puts "Found: #{even}"

  # Doubly Linked List
  puts "\n2. DOUBLY LINKED LIST"
  puts '-' * 80
  dll = DoublyLinkedList.new

  puts 'Inserting: A, B, C at head'
  dll.insert_at_head('C')
  dll.insert_at_head('B')
  dll.insert_at_head('A')
  puts "List: #{dll}"

  puts "\nInserting: D, E at tail"
  dll.insert_at_tail('D')
  dll.insert_at_tail('E')
  puts "List: #{dll}"

  puts "\nForward iteration: #{dll.to_a}"
  puts "Backward iteration: #{dll.reverse_each.to_a}"

  # Circular Linked List
  puts "\n3. CIRCULAR LINKED LIST"
  puts '-' * 80
  cll = CircularLinkedList.new

  puts 'Inserting: 1, 2, 3, 4, 5'
  (1..5).each { |i| cll.insert_at_tail(i) }
  puts "List: #{cll}"

  # Skip List
  puts "\n4. SKIP LIST"
  puts '-' * 80
  sl = SkipList.new

  puts 'Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6'
  [3, 7, 1, 9, 5, 2, 8, 4, 6].each { |val| sl.insert(val) }

  puts "Skip list (sorted): #{sl}"

  puts "\nSearching for 5: #{sl.search(5)}"
  puts "Searching for 10: #{sl.search(10)}"

  puts "\nDeleting 5..."
  sl.delete(5)
  puts "Skip list: #{sl}"

  puts "\n#{'=' * 80}"
  puts '✨ All demonstrations complete!'
  puts '=' * 80
end

demonstrate if __FILE__ == $PROGRAM_NAME
