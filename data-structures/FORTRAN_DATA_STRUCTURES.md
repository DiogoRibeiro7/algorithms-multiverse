# Fortran Data Structures

Comprehensive implementations of fundamental data structures in Modern Fortran (Fortran 90/95/2003/2008).

## Overview

This collection demonstrates how to implement classic data structures in Fortran using modern features including:
- Type-bound procedures (OOP)
- Pointers and dynamic allocation
- Recursive procedures
- Modules and encapsulation

## Implemented Data Structures

### 1. Binary Search Tree (BST)
**File**: `bst.f90`

A complete implementation of a binary search tree with full operations.

**Features**:
- Insert, search, delete operations
- Tree traversals (inorder, preorder, postorder, level-order)
- Min/max/height calculations
- Balance checking
- Tree visualization

**Type Definition**:
```fortran
type :: binary_search_tree
    type(bst_node), pointer :: root => null()
    integer :: node_count = 0
contains
    procedure :: insert
    procedure :: search
    procedure :: delete
    procedure :: find_min
    procedure :: find_max
    procedure :: get_height
    procedure :: is_balanced
    procedure :: inorder_traversal
    procedure :: print_tree
end type
```

**Usage Example**:
```fortran
use bst_module
type(binary_search_tree) :: tree

call tree%insert(50, 50.0d0)
call tree%insert(30, 30.0d0)
call tree%insert(70, 70.0d0)

if (tree%search(30)) then
    print *, 'Found 30'
end if

call tree%inorder_traversal()  ! Prints: 30 50 70
print *, 'Height:', tree%get_height()
```

**Complexity**:
| Operation | Average | Worst Case |
|-----------|---------|------------|
| Search    | O(log n)| O(n)       |
| Insert    | O(log n)| O(n)       |
| Delete    | O(log n)| O(n)       |
| Traversal | O(n)    | O(n)       |

**Applications**:
- Dictionary implementations
- Database indexing
- Expression trees
- Huffman coding trees

---

### 2. Stack
**File**: `stack.f90`

Dual implementation with both array-based and linked-list approaches.

**Features**:
- Array-based stack (fixed size, O(1) operations)
- Linked-list-based stack (dynamic size, O(1) operations)
- Bracket matching application
- String reversal
- Postfix expression evaluation

**Type Definitions**:
```fortran
! Array-based
type :: array_stack
    integer :: data(STACK_MAX_SIZE)
    integer :: top = 0
contains
    procedure :: push
    procedure :: pop
    procedure :: peek
    procedure :: is_empty
    procedure :: is_full
end type

! Linked-list-based
type :: linked_stack
    type(stack_node), pointer :: top => null()
    integer :: size = 0
contains
    procedure :: push
    procedure :: pop
    procedure :: peek
    procedure :: is_empty
end type
```

**Usage Example**:
```fortran
use stack_module
type(array_stack) :: stack

call stack%push(10)
call stack%push(20)
call stack%push(30)

print *, stack%peek()  ! 30
value = stack%pop()     ! 30
print *, stack%get_size()  ! 2

! Bracket matching
if (is_balanced('{[()]}')) then
    print *, 'Balanced!'
end if
```

**Complexity**:
| Operation | Array-based | Linked-list |
|-----------|-------------|-------------|
| Push      | O(1)        | O(1)        |
| Pop       | O(1)        | O(1)        |
| Peek      | O(1)        | O(1)        |
| Space     | O(n)        | O(n)        |

**Applications**:
- Expression evaluation
- Function call management
- Backtracking algorithms (DFS, maze solving)
- Undo/Redo operations
- Browser history

---

### 3. Queue
**File**: `queue.f90`

Comprehensive queue implementation with multiple variants.

**Features**:
- Circular array-based queue (efficient space usage)
- Linked-list-based queue (unlimited size)
- Priority queue (min-heap implementation)
- Deque (double-ended queue)

**Type Definitions**:
```fortran
! Circular queue
type :: array_queue
    integer :: data(QUEUE_MAX_SIZE)
    integer :: front = 1
    integer :: rear = 0
    integer :: size = 0
contains
    procedure :: enqueue
    procedure :: dequeue
    procedure :: get_front
    procedure :: is_empty
end type

! Priority queue
type :: priority_queue
    integer :: data(QUEUE_MAX_SIZE)
    integer :: size = 0
contains
    procedure :: insert
    procedure :: extract_min
    procedure :: get_min
end type

! Deque
type :: deque
contains
    procedure :: push_front
    procedure :: push_back
    procedure :: pop_front
    procedure :: pop_back
end type
```

**Usage Example**:
```fortran
use queue_module

! Regular queue
type(array_queue) :: queue
call queue%enqueue(10)
call queue%enqueue(20)
value = queue%dequeue()  ! 10

! Priority queue
type(priority_queue) :: pq
call pq%insert(50)
call pq%insert(30)
call pq%insert(70)
min_val = pq%extract_min()  ! 30

! Deque
type(deque) :: dq
call dq%push_front(10)
call dq%push_back(20)
```

**Complexity**:
| Type           | Enqueue/Insert | Dequeue/Extract | Front/Min | Space |
|----------------|----------------|-----------------|-----------|-------|
| Array Queue    | O(1)           | O(1)            | O(1)      | O(n)  |
| Linked Queue   | O(1)           | O(1)            | O(1)      | O(n)  |
| Priority Queue | O(log n)       | O(log n)        | O(1)      | O(n)  |
| Deque          | O(1)           | O(1)            | O(1)      | O(n)  |

**Applications**:
- Task scheduling (FIFO)
- Breadth-First Search (BFS)
- Print spooling
- Request handling in servers
- Priority Queue: Dijkstra's algorithm, event simulation
- Deque: Sliding window problems

---

### 4. Trie (Prefix Tree)
**File**: `trie.f90`

Array-based trie implementation for efficient prefix matching.

**Features**:
- Insert, search, startsWith operations
- Word counting
- Prefix matching and counting
- Auto-complete functionality
- Case-insensitive

**Note**: This is a simplified array-based implementation. A full pointer-based trie would be more memory-efficient but complex in Fortran due to limited support for arrays of pointers.

**Type Definition**:
```fortran
type :: trie
    character(len=MAX_WORD_LENGTH) :: words(MAX_WORDS)
    integer :: word_count = 0
contains
    procedure :: insert
    procedure :: search
    procedure :: starts_with
    procedure :: delete
    procedure :: count_words
    procedure :: count_prefix
    procedure :: get_words_with_prefix
    procedure :: print_all
end type
```

**Usage Example**:
```fortran
use trie_module
type(trie) :: dictionary

call dictionary%insert('the')
call dictionary%insert('there')
call dictionary%insert('their')

if (dictionary%search('the')) then
    print *, 'Found!'
end if

if (dictionary%starts_with('th')) then
    print *, 'Words starting with "th":'
    call dictionary%get_words_with_prefix('th')
end if

count = dictionary%count_prefix('th')  ! 3
```

**Complexity** (Array-based implementation):
| Operation    | Time     | Space |
|--------------|----------|-------|
| Insert       | O(n*m)   | O(n*m)|
| Search       | O(n*m)   | O(1)  |
| Delete       | O(n*m)   | O(1)  |
| Prefix Match | O(n*m)   | O(1)  |

where n = number of words, m = length of word/prefix

**Note**: A pointer-based trie would have O(m) insert/search time.

**Applications**:
- Auto-complete / Type-ahead search
- Spell checking
- IP routing (longest prefix matching)
- Dictionary implementation
- T9 predictive text
- Genome sequence analysis

---

## Building and Running

### Individual Programs

```bash
# Binary Search Tree
cd data-structures
gfortran -O2 -o bst_test bst.f90
./bst_test

# Stack
gfortran -O2 -o stack_test stack.f90
./stack_test

# Queue
gfortran -O2 -o queue_test queue.f90
./queue_test

# Trie
gfortran -O2 -o trie_test trie.f90
./trie_test
```

### All Data Structures

Run the comprehensive test suite:

```bash
chmod +x test_all_fortran_ds.sh
./test_all_fortran_ds.sh
```

This will compile and test all data structures, providing:
- Compilation status for each
- Test execution results
- Sample output from each test
- Summary statistics

## Modern Fortran Features Used

### 1. Type-Bound Procedures (OOP)
```fortran
type :: stack
    integer :: data(100)
    integer :: top = 0
contains
    procedure :: push => stack_push
    procedure :: pop => stack_pop
end type
```

### 2. Pointers and Dynamic Allocation
```fortran
type :: bst_node
    integer :: key
    type(bst_node), pointer :: left => null()
    type(bst_node), pointer :: right => null()
end type

allocate(new_node)
new_node%left => null()
```

### 3. Recursive Procedures
```fortran
recursive function search_recursive(node, key) result(found)
    type(bst_node), pointer, intent(in) :: node
    integer, intent(in) :: key
    type(bst_node), pointer :: found

    if (key < node%key) then
        found => search_recursive(node%left, key)
    else
        found => search_recursive(node%right, key)
    end if
end function
```

### 4. Intent Specifications
```fortran
subroutine insert(this, value)
    class(stack), intent(inout) :: this
    integer, intent(in) :: value
    ! ...
end subroutine
```

## Design Patterns

### 1. Encapsulation
All data structures use private members with public interfaces:
```fortran
type :: queue
    private
    integer :: data(100)
    integer :: front, rear
contains
    procedure, public :: enqueue
    procedure, public :: dequeue
end type
```

### 2. Iterator Pattern (via Traversals)
```fortran
call tree%inorder_traversal()
call tree%preorder_traversal()
call tree%postorder_traversal()
call tree%level_order()
```

### 3. Factory Pattern (Initialization)
```fortran
type(binary_search_tree) :: tree
! Automatic initialization via default values
tree%root => null()
tree%node_count = 0
```

## Best Practices Demonstrated

1. **Memory Management**:
   - Proper allocation/deallocation
   - Cleanup procedures (destroy methods)
   - Null pointer initialization

2. **Error Handling**:
   - Overflow/underflow checks
   - Empty container checks
   - Invalid operation handling

3. **Code Organization**:
   - Modules for encapsulation
   - Logical grouping of procedures
   - Consistent naming conventions

4. **Documentation**:
   - Inline comments explaining algorithms
   - Complexity analysis in comments
   - Usage examples in test programs

## Performance Considerations

### Array-based vs. Linked Structures

**Array-based** (Stack, Queue):
- Pros: Cache-friendly, O(1) access, no allocation overhead
- Cons: Fixed size, wasted space

**Linked** (BST, Linked Stack/Queue):
- Pros: Dynamic size, efficient insertions/deletions
- Cons: Extra memory for pointers, pointer chasing

### Optimization Tips

1. **Use `-O2` or `-O3` compiler flags**:
   ```bash
   gfortran -O3 -o program program.f90
   ```

2. **For large datasets, use 64-bit integers**:
   ```fortran
   integer(8) :: large_value
   ```

3. **Inline small functions** (compiler usually does this automatically)

4. **Minimize pointer chasing**:
   - Prefer array-based when size is known
   - Use iterative over recursive when possible

## Limitations and Extensions

### Current Limitations

1. **Fixed sizes** for array-based structures
2. **No generic/template** support (Fortran limitation)
3. **Integer-only** data (can be extended to other types)
4. **Trie** uses simplified array-based approach

### Possible Extensions

1. **Generic Data Types**:
   - Use preprocessor macros
   - Create separate modules for different types

2. **Self-Balancing Trees**:
   - Implement AVL tree
   - Implement Red-Black tree

3. **Advanced Features**:
   - Persistent data structures
   - Concurrent/thread-safe versions
   - Iterator interfaces

4. **True Pointer-based Trie**:
   - Use derived types with allocatable arrays
   - More complex but more efficient

## Comparison with Other Languages

| Feature              | Fortran | C/C++ | Python |
|----------------------|---------|-------|--------|
| Manual Memory Mgmt   | Yes     | Yes   | No     |
| OOP Support          | Modern  | Full  | Full   |
| Pointers             | Yes     | Yes   | No     |
| Recursion            | Yes     | Yes   | Yes    |
| Templates/Generics   | No      | Yes   | Yes    |
| Dynamic Typing       | No      | No    | Yes    |

## Testing

Each implementation includes:
- Basic operations testing
- Edge case validation (empty, full, single element)
- Application demonstrations
- Performance characteristics display

Run individual tests:
```bash
./bst_test      # BST with tree visualization
./stack_test    # Stack with bracket matching
./queue_test    # Queue variants
./trie_test     # Trie with auto-complete
```

## References

### Data Structures Theory
- **Introduction to Algorithms** (CLRS)
- **Data Structures and Algorithm Analysis** (Mark Allen Weiss)
- **The Art of Computer Programming** (Donald Knuth)

### Fortran Programming
- **Modern Fortran Explained** (Metcalf, Reid, Cohen)
- **Fortran 95/2003 for Scientists and Engineers** (Stephen Chapman)
- **Modern Fortran: Building Efficient Parallel Applications** (Milan Curcic)

### Online Resources
- Fortran Wiki: https://fortranwiki.org
- Fortran Standards: https://wg5-fortran.org
- Rosetta Code: https://rosettacode.org

## License

See root LICENSE file for details.

## Contributing

When adding new data structures:
1. Follow existing code style
2. Include comprehensive tests
3. Add complexity analysis
4. Provide usage examples
5. Update this documentation

## Contact

For questions or contributions, please refer to the repository's issue tracker.

---

**Last Updated**: 2025
**Fortran Standard**: Fortran 90/95/2003/2008
**Compiler Tested**: GNU Fortran (GCC) 13.2.0
**Status**: Production Ready
