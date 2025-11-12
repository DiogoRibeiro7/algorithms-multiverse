# 🎓 Learning Path: From Beginner to Algorithm Expert

**A structured, progressive guide to mastering algorithms and data structures.**

---

## 📑 Table of Contents

- [How to Use This Guide](#how-to-use-this-guide)
- [Level 0: Prerequisites](#level-0-prerequisites)
- [Level 1: Foundations (Beginner)](#level-1-foundations-beginner)
- [Level 2: Core Algorithms (Intermediate)](#level-2-core-algorithms-intermediate)
- [Level 3: Advanced Techniques (Advanced)](#level-3-advanced-techniques-advanced)
- [Level 4: Expert Topics (Expert)](#level-4-expert-topics-expert)
- [Practice Resources](#practice-resources)
- [Interview Preparation Track](#interview-preparation-track)
- [Competitive Programming Track](#competitive-programming-track)

---

## How to Use This Guide

### General Approach

1. **Start at your level** - Don't skip foundations
2. **Complete each topic** before moving to the next
3. **Implement in your preferred language** first, then try others
4. **Test your understanding** - Run the provided test cases
5. **Practice problems** - Solve related problems on coding platforms
6. **Build projects** - Apply algorithms to real problems

### Time Estimates

| Level | Estimated Time | Prerequisites |
|-------|---------------|---------------|
| Level 0 | 1-2 weeks | None |
| Level 1 | 4-6 weeks | Level 0 |
| Level 2 | 8-12 weeks | Level 1 |
| Level 3 | 12-16 weeks | Level 2 |
| Level 4 | Ongoing | Level 3 |

### Learning Methods

For each algorithm:
1. 📖 **Read** the theory and complexity analysis
2. 👀 **Watch** it in the [visualizer](./visualizer/)
3. 💻 **Implement** it yourself (don't just copy!)
4. 🧪 **Test** with edge cases
5. 📊 **Compare** with other implementations
6. 🎯 **Practice** related problems

---

## Level 0: Prerequisites

**Goal**: Build foundation for algorithmic thinking

### Programming Basics (Choose ONE language to start)

**Recommended for beginners**: Python or JavaScript

✅ **Variables and Data Types**
- Integers, floats, strings, booleans
- Type conversions

✅ **Control Flow**
- If/else statements
- Switch/case statements
- Conditional expressions

✅ **Loops**
- For loops
- While loops
- Loop control (break, continue)

✅ **Functions**
- Function definition and calls
- Parameters and return values
- Scope and closures

✅ **Basic Data Structures** (language built-ins)
- Arrays/Lists
- Strings
- Dictionaries/Maps/Objects
- Sets

### Mathematical Foundations

✅ **Basics**
- Arithmetic operations
- Exponents and logarithms
- Modular arithmetic (%, mod)

✅ **Logic**
- Boolean algebra
- Logical operators (AND, OR, NOT)
- Truth tables

### Problem-Solving Skills

✅ **Decomposition** - Breaking problems into smaller parts
✅ **Pattern Recognition** - Identifying similar problems
✅ **Abstraction** - Generalizing solutions
✅ **Algorithm Design** - Step-by-step planning

### Practice

- Solve 10-20 simple problems on [HackerRank Easy](https://www.hackerrank.com/)
- Complete basic Python/JS exercises
- Write simple functions (sum array, find max, reverse string)

---

## Level 1: Foundations (Beginner)

**Goal**: Master basic algorithms and understand complexity

**Estimated Time**: 4-6 weeks

### Week 1-2: Arrays and Basic Algorithms

#### Topics

✅ **Array Operations**
- Traversal (iteration)
- Insertion and deletion
- Searching in arrays
- Two-pointer technique

**Start Here**:
```bash
cd sorting/
python3 bubble_sort.py  # Understand the simplest sort

cd visualizer/
python -m http.server 8080  # See it in action
```

#### Algorithms to Learn

1. **Linear Search** [`searching/`]
   - Time: O(n), Space: O(1)
   - Practice: Find element in unsorted array

2. **Binary Search** [`searching/`]
   - Time: O(log n), Space: O(1)
   - ⚠️ Requires sorted array!
   - Practice: Find element in sorted array

3. **Bubble Sort** [`sorting/bubble_sort.*`]
   - Time: O(n²), Space: O(1)
   - Understand swapping and iteration

4. **Selection Sort** [`sorting/selection_sort.*`]
   - Time: O(n²), Space: O(1)
   - Understand finding minimum

5. **Insertion Sort** [`sorting/insertion_sort.*`]
   - Time: O(n²), Space: O(1)
   - Good for small/nearly sorted data

#### Practice Problems

- Reverse an array
- Find maximum/minimum
- Remove duplicates from sorted array
- Rotate array by k positions
- Two sum problem
- Best time to buy/sell stock

#### Milestones

- [ ] Implemented all 5 algorithms
- [ ] Understood Big O notation basics
- [ ] Solved 15+ easy array problems
- [ ] Can explain when to use binary vs linear search

### Week 3-4: Basic Data Structures

#### Topics

✅ **Strings**
- String manipulation
- Character arrays
- String matching basics

✅ **Stacks** [`data-structures/stack_queue.py`]
- LIFO (Last In, First Out)
- Push, pop, peek operations
- Applications: parentheses matching, undo operations

✅ **Queues** [`data-structures/stack_queue.py`]
- FIFO (First In, First Out)
- Enqueue, dequeue operations
- Applications: BFS, task scheduling

✅ **Linked Lists** [`data-structures/linked_list.*`]
- Singly linked lists
- Doubly linked lists
- Insertion, deletion, traversal

#### Algorithms to Learn

1. **String Reversal**
   - Multiple approaches

2. **Valid Parentheses** (using stack)
   - Time: O(n), Space: O(n)

3. **Queue using Stacks**
   - Amortized O(1) operations

4. **Linked List Operations**
   - Reverse linked list
   - Detect cycle (Floyd's algorithm)
   - Find middle element

#### Practice Problems

- Implement stack using array
- Implement queue using array
- Reverse linked list
- Merge two sorted linked lists
- Remove nth node from end
- Palindrome linked list

#### Milestones

- [ ] Implemented stack and queue from scratch
- [ ] Comfortable with linked list operations
- [ ] Solved 20+ easy problems
- [ ] Understand when to use array vs linked list

### Week 5-6: Introduction to Recursion

#### Topics

✅ **Recursion Basics**
- Base case and recursive case
- Call stack visualization
- Tail recursion

✅ **Common Patterns**
- Counting/accumulation
- Generation (permutations, combinations)
- Divide and conquer basics

#### Algorithms to Learn

1. **Factorial** (classic intro)
   - Time: O(n), Space: O(n) call stack

2. **Fibonacci** (naive → optimized)
   - Naive: O(2ⁿ)
   - Memoized: O(n)

3. **Power Function**
   - Naive: O(n)
   - Optimized: O(log n)

4. **Sum of Array** (recursive)
   - Time: O(n), Space: O(n)

#### Practice Problems

- Sum of digits
- Reverse a string (recursively)
- Check if string is palindrome
- Tower of Hanoi
- Generate all binary strings of length n

#### Milestones

- [ ] Understand base case and recursive case
- [ ] Can trace recursive calls on paper
- [ ] Know difference between recursion and iteration
- [ ] Solved 10+ recursion problems

---

## Level 2: Core Algorithms (Intermediate)

**Goal**: Master essential algorithms and data structures

**Estimated Time**: 8-12 weeks

### Month 1: Efficient Sorting and Searching

#### Sorting Algorithms

1. **Merge Sort** [`sorting/merge_sort.*`]
   - Divide and conquer
   - Time: O(n log n), Space: O(n)
   - Stable sort
   - **Master Theorem practice**

2. **Quick Sort** [`sorting/quick_sort.*`]
   - Divide and conquer with pivot
   - Average: O(n log n), Worst: O(n²)
   - In-place sorting
   - Partition technique

3. **Heap Sort** [`sorting/heap_sort.*`]
   - Using heap data structure
   - Time: O(n log n), Space: O(1)
   - Not stable

#### Advanced Searching

1. **Binary Search Variants**
   - First/last occurrence
   - Search in rotated array
   - Search 2D matrix

2. **Jump Search**
   - Time: O(√n)
   - Block jumping

3. **Interpolation Search**
   - Time: O(log log n) for uniform data
   - Position estimation

#### Practice Problems

- Merge k sorted arrays
- Kth largest element
- Find peak element
- Search in rotated sorted array
- Median of two sorted arrays

#### Milestones

- [ ] Implemented merge and quick sort
- [ ] Understand divide and conquer
- [ ] Can analyze recurrence relations
- [ ] Solved 30+ medium problems

### Month 2: Trees and Tree Algorithms

#### Topics

✅ **Binary Trees** [`data-structures/binary_tree.*`]
- Tree traversals (inorder, preorder, postorder, level-order)
- Height and depth
- Binary tree properties

✅ **Binary Search Trees**
- BST property
- Insert, delete, search
- Time: O(log n) average, O(n) worst

✅ **Balanced Trees** (concepts)
- AVL trees
- Red-Black trees
- Why balancing matters

#### Algorithms to Learn

1. **Tree Traversals**
   - Inorder: Left → Root → Right
   - Preorder: Root → Left → Right
   - Postorder: Left → Right → Root
   - Level-order (BFS)

2. **BST Operations**
   - Insert: O(log n) average
   - Search: O(log n) average
   - Delete: O(log n) average

3. **Tree Problems**
   - Maximum depth
   - Same tree check
   - Symmetric tree
   - Path sum
   - Lowest common ancestor

#### Practice with Visualizer

```bash
cd visualizer/
# Select "Trees" tab
# Try different traversals on BST
# Compare Complete vs Balanced trees
```

#### Practice Problems

- Validate BST
- Invert binary tree
- Diameter of binary tree
- Serialize and deserialize tree
- Binary tree right side view

#### Milestones

- [ ] Implemented all tree traversals
- [ ] Built BST from scratch
- [ ] Understand tree recursion
- [ ] Solved 25+ tree problems

### Month 3: Graph Algorithms

#### Topics

✅ **Graph Representations**
- Adjacency matrix
- Adjacency list
- Edge list

✅ **Graph Traversals** [`graph-algorithms/`]
- **BFS** (Breadth-First Search)
  - Level-by-level exploration
  - Queue-based
  - Time: O(V + E)
  - Shortest path in unweighted graph

- **DFS** (Depth-First Search)
  - Go deep first
  - Stack-based (or recursive)
  - Time: O(V + E)
  - Cycle detection, topological sort

#### Algorithms to Learn

1. **BFS Applications**
   - Shortest path (unweighted)
   - Level-order traversal
   - Connected components

2. **DFS Applications**
   - Cycle detection
   - Topological sorting
   - Path finding

3. **Basic Graph Problems**
   - Number of islands
   - Clone graph
   - Course schedule (topological sort)

#### Practice Problems

- Number of connected components
- Is graph bipartite?
- Course schedule I & II
- Number of provinces
- Flood fill

#### Milestones

- [ ] Implemented BFS and DFS
- [ ] Understand graph representations
- [ ] Can detect cycles
- [ ] Solved 20+ graph problems

---

## Level 3: Advanced Techniques (Advanced)

**Goal**: Master advanced algorithms and problem-solving techniques

**Estimated Time**: 12-16 weeks

### Advanced Topic 1: Dynamic Programming

**⚠️ This is challenging! Take your time.**

#### Introduction to DP

Dynamic Programming = **Recursion + Memoization**

**Key Characteristics**:
1. **Optimal Substructure** - Optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems** - Same subproblems solved multiple times

#### DP Approaches

1. **Top-Down (Memoization)**
   - Recursive with caching
   - Natural problem decomposition

2. **Bottom-Up (Tabulation)**
   - Iterative table filling
   - Often more efficient

#### Classic DP Problems

1. **Fibonacci** (intro)
   - Naive: O(2ⁿ)
   - DP: O(n)

2. **Climbing Stairs**
   - Entry-level DP

3. **Coin Change** [`dynamic-programming/`]
   - Minimum coins to make amount
   - Classic DP

4. **0/1 Knapsack** [`dynamic-programming/knapsack.*`]
   - Maximize value with weight constraint
   - 2D DP table

5. **Longest Common Subsequence** [`dynamic-programming/`]
   - String matching
   - 2D DP table

6. **Edit Distance** [`dynamic-programming/edit_distance.*`]
   - Minimum operations to transform
   - Levenshtein distance

#### Learning Strategy

1. **Identify** if problem needs DP:
   - "Minimum/Maximum/Longest/Count ways"
   - Overlapping subproblems

2. **Define** DP state:
   - What information do we need?
   - `dp[i]` = answer for subproblem of size i

3. **Find** recurrence relation:
   - How to build dp[i] from smaller subproblems?

4. **Determine** base cases:
   - dp[0], dp[1], etc.

5. **Implement** top-down or bottom-up

#### Practice Problems

- House robber
- Unique paths
- Longest increasing subsequence
- Partition equal subset sum
- Word break

#### Milestones

- [ ] Solved 30+ DP problems
- [ ] Can identify DP problems
- [ ] Comfortable with 1D and 2D DP
- [ ] Understand memoization vs tabulation

### Advanced Topic 2: Advanced Graph Algorithms

#### Shortest Path Algorithms

1. **Dijkstra's Algorithm** [`graph-algorithms/dijkstra.*`]
   - Single-source shortest path
   - Non-negative weights
   - Time: O(E log V) with priority queue

2. **Bellman-Ford**
   - Handles negative weights
   - Detects negative cycles
   - Time: O(VE)

3. **Floyd-Warshall**
   - All-pairs shortest path
   - Time: O(V³)

4. **A* Search**
   - Heuristic-based shortest path
   - Game pathfinding

#### Minimum Spanning Tree

1. **Kruskal's Algorithm** [`graph-algorithms/mst.*`]
   - Edge-based, uses Union-Find
   - Time: O(E log E)

2. **Prim's Algorithm** [`graph-algorithms/mst.*`]
   - Vertex-based, uses priority queue
   - Time: O(E log V)

#### Advanced Topics

- Strongly connected components (Kosaraju, Tarjan)
- Articulation points and bridges
- Network flow (Ford-Fulkerson)

#### Practice Problems

- Cheapest flights within k stops
- Network delay time
- Reconstruct itinerary
- Critical connections

#### Milestones

- [ ] Implemented Dijkstra's and MST
- [ ] Understand Union-Find
- [ ] Solved 25+ advanced graph problems

### Advanced Topic 3: Advanced Data Structures

#### Heaps and Priority Queues

1. **Binary Heap**
   - Insert: O(log n)
   - Extract min/max: O(log n)
   - Build heap: O(n)

2. **Applications**
   - Top K elements
   - Median finder
   - Task scheduling

#### Tries (Prefix Trees)

1. **Trie Operations** [`data-structures/prefix_tree.py`]
   - Insert: O(m) where m = word length
   - Search: O(m)
   - Applications: autocomplete, spell check

#### Advanced Structures (concepts)

- Segment Trees (range queries)
- Fenwick Trees (Binary Indexed Tree)
- Disjoint Set Union (Union-Find)

#### Practice Problems

- Kth largest element in stream
- Find median from data stream
- Implement Trie
- Word search II
- Design search autocomplete

#### Milestones

- [ ] Implemented heap from scratch
- [ ] Built trie from scratch
- [ ] Understand when to use each structure
- [ ] Solved 20+ problems

---

## Level 4: Expert Topics (Expert)

**Goal**: Competitive programming and specialized algorithms

**Estimated Time**: Ongoing

### Expert Topic 1: String Algorithms

1. **KMP Pattern Matching** [`string-algorithms/`]
   - Time: O(n + m)
   - Failure function

2. **Rabin-Karp**
   - Rolling hash
   - Multiple pattern matching

3. **Suffix Arrays and Trees**
   - Advanced string indexing

4. **Manacher's Algorithm**
   - Longest palindromic substring
   - Time: O(n)

### Expert Topic 2: Advanced DP Patterns

- Bitmask DP
- Digit DP
- DP on trees
- State compression

### Expert Topic 3: Computational Geometry

[`computational-geometry/`]
- Convex hull (Graham scan)
- Line intersection
- Point in polygon
- Closest pair of points

### Expert Topic 4: Number Theory

[`number-theory/`]
- Prime sieves
- GCD and LCM
- Modular arithmetic
- Fast exponentiation
- Chinese Remainder Theorem

### Expert Topic 5: Game Theory

- Nim game
- Minimax algorithm
- Alpha-beta pruning

---

## Practice Resources

### Coding Platforms (Ordered by Difficulty)

| Platform | Best For | Difficulty |
|----------|----------|------------|
| [HackerRank](https://hackerrank.com) | Beginners, structured learning | Easy → Medium |
| [LeetCode](https://leetcode.com) | Interview prep, problem variety | Easy → Hard |
| [Codeforces](https://codeforces.com) | Competitive programming | Medium → Expert |
| [AtCoder](https://atcoder.jp) | High-quality contests | Medium → Expert |
| [CodeChef](https://codechef.com) | Long contests, learning | Easy → Hard |
| [TopCoder](https://topcoder.com) | SRMs, advanced problems | Hard |

### Problem Sets

**Beginner** (Level 0-1):
- [LeetCode Easy Problems](https://leetcode.com/problemset/all/?difficulty=Easy)
- [HackerRank Easy Algorithms](https://www.hackerrank.com/domains/algorithms)

**Intermediate** (Level 2):
- [Grind 75](https://www.techinterviewhandbook.org/grind75) - Curated interview prep
- [LeetCode Top 100 Liked](https://leetcode.com/problemset/top-100-liked-questions/)

**Advanced** (Level 3-4):
- [LeetCode Hard Problems](https://leetcode.com/problemset/all/?difficulty=Hard)
- [Codeforces Problem Set](https://codeforces.com/problemset)

---

## Interview Preparation Track

**Timeline**: 8-12 weeks intensive

### Week 1-2: Arrays and Strings
- Two pointers
- Sliding window
- Hash tables

### Week 3-4: Linked Lists and Stacks/Queues
- Fast/slow pointers
- Dummy nodes
- Monotonic stack

### Week 5-6: Trees and Graphs
- BFS/DFS
- Binary search trees
- Graph traversals

### Week 7-8: Dynamic Programming
- 1D DP
- 2D DP
- Common patterns

### Week 9-10: Advanced Topics
- Heaps
- Tries
- Advanced graphs

### Week 11-12: System Design & Review
- Mock interviews
- Problem solving under time pressure
- Review weak areas

### Recommended Problem Count

- Easy: 50-100 problems
- Medium: 100-150 problems
- Hard: 20-30 problems

**Total**: ~200-280 problems

---

## Competitive Programming Track

### Getting Started

1. **Learn C++ or Java** (faster I/O)
2. **Master templates** for common operations
3. **Practice typing speed** and accuracy
4. **Learn to read editorials**

### Contest Strategy

1. **Read all problems** quickly
2. **Solve easiest first** (maximum points early)
3. **Skip and return** to hard problems
4. **Test with edge cases** before submitting
5. **Manage time** wisely

### Training Schedule

- **Daily**: 1-2 hours problem solving
- **Weekly**: 2-3 contests
- **Monthly**: Review and learn new techniques

### Progression

1. **Division 4** (Beginner) - Codeforces
2. **Division 3** (Intermediate)
3. **Division 2** (Advanced)
4. **Division 1** (Expert)

---

## Recommended Books

### Beginner
- "Grokking Algorithms" by Aditya Bhargava
- "Cracking the Coding Interview" by Gayle McDowell

### Intermediate
- "Algorithm Design Manual" by Steven Skiena
- "Elements of Programming Interviews" (Python/Java/C++)

### Advanced
- "Introduction to Algorithms" (CLRS)
- "Competitive Programming" by Steven & Felix Halim

---

## Progress Tracking

### Checkpoints

**After Level 1**: Can you...
- [ ] Implement binary search without bugs?
- [ ] Explain Big O for common operations?
- [ ] Reverse a linked list?
- [ ] Use a stack to solve a problem?

**After Level 2**: Can you...
- [ ] Implement merge sort and quick sort?
- [ ] Traverse a tree in multiple ways?
- [ ] Implement BFS and DFS?
- [ ] Recognize when to use which data structure?

**After Level 3**: Can you...
- [ ] Solve most DP problems?
- [ ] Implement Dijkstra's algorithm?
- [ ] Design optimal solutions?
- [ ] Analyze time and space complexity accurately?

---

## Final Tips

1. **Consistency > Intensity**: 1 hour daily beats 8 hours on Sunday
2. **Understand, don't memorize**: Focus on patterns, not solutions
3. **Code without IDE**: Practice on paper or simple editors
4. **Explain your solutions**: Teach others or write explanations
5. **Review regularly**: Spaced repetition for retention
6. **Don't give up**: It's okay to look at solutions after trying
7. **Join communities**: Learn from others, ask questions
8. **Track progress**: Keep a log of problems solved

---

**Next Steps**: Start with [Level 0](#level-0-prerequisites) if you're new, or jump to your appropriate level!

**[⬆ Back to Main README](./README.md)** | **[COMPLEXITY_GUIDE.md](./COMPLEXITY_GUIDE.md)** | **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)**
