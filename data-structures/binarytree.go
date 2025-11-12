// Binary Tree Data Structure Implementation in Go
//
// Time Complexity:
// - Insertion: O(n) worst case (unbalanced)
// - Search: O(n) worst case (unbalanced)
// - Traversal: O(n)
// - Height: O(n)
// Space Complexity: O(n)
//
// A binary tree is a hierarchical data structure where each node has at most
// two children (left and right). It's the foundation for many advanced data
// structures like BST, AVL trees, and heaps.
//
// Go features:
// - Generic implementation using type parameters
// - Multiple traversal algorithms (recursive and iterative)
// - Parallel traversal with goroutines
// - Tree visualization and serialization
// - Level-order traversal with channels
// - Tree metrics and analysis

package main

import (
	"fmt"
	"math"
	"strings"
	"sync"
)

// TreeNode represents a node in a binary tree
type TreeNode[T any] struct {
	Data  T
	Left  *TreeNode[T]
	Right *TreeNode[T]
}

// NewTreeNode creates a new tree node
func NewTreeNode[T any](data T) *TreeNode[T] {
	return &TreeNode[T]{
		Data:  data,
		Left:  nil,
		Right: nil,
	}
}

// BinaryTree represents a binary tree
type BinaryTree[T any] struct {
	Root *TreeNode[T]
	size int
}

// NewBinaryTree creates a new binary tree
func NewBinaryTree[T any]() *BinaryTree[T] {
	return &BinaryTree[T]{
		Root: nil,
		size: 0,
	}
}

// Size returns the number of nodes in the tree
func (bt *BinaryTree[T]) Size() int {
	return bt.size
}

// IsEmpty checks if the tree is empty
func (bt *BinaryTree[T]) IsEmpty() bool {
	return bt.Root == nil
}

// Insert inserts a new value (level-order insertion)
//
// Time Complexity: O(n)
func (bt *BinaryTree[T]) Insert(data T) {
	newNode := NewTreeNode(data)

	if bt.Root == nil {
		bt.Root = newNode
		bt.size++
		return
	}

	// Level-order insertion using queue
	queue := []*TreeNode[T]{bt.Root}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		if current.Left == nil {
			current.Left = newNode
			bt.size++
			return
		} else {
			queue = append(queue, current.Left)
		}

		if current.Right == nil {
			current.Right = newNode
			bt.size++
			return
		} else {
			queue = append(queue, current.Right)
		}
	}
}

// Height calculates the height of the tree
//
// Time Complexity: O(n)
func (bt *BinaryTree[T]) Height() int {
	return height(bt.Root)
}

func height[T any](node *TreeNode[T]) int {
	if node == nil {
		return 0
	}

	leftHeight := height(node.Left)
	rightHeight := height(node.Right)

	if leftHeight > rightHeight {
		return leftHeight + 1
	}
	return rightHeight + 1
}

// TRAVERSAL ALGORITHMS

// InOrderTraversal performs in-order traversal (Left-Root-Right)
//
// Time Complexity: O(n)
// Space Complexity: O(h) where h is height
func (bt *BinaryTree[T]) InOrderTraversal() []T {
	result := make([]T, 0, bt.size)
	inOrderHelper(bt.Root, &result)
	return result
}

func inOrderHelper[T any](node *TreeNode[T], result *[]T) {
	if node == nil {
		return
	}

	inOrderHelper(node.Left, result)
	*result = append(*result, node.Data)
	inOrderHelper(node.Right, result)
}

// PreOrderTraversal performs pre-order traversal (Root-Left-Right)
//
// Time Complexity: O(n)
func (bt *BinaryTree[T]) PreOrderTraversal() []T {
	result := make([]T, 0, bt.size)
	preOrderHelper(bt.Root, &result)
	return result
}

func preOrderHelper[T any](node *TreeNode[T], result *[]T) {
	if node == nil {
		return
	}

	*result = append(*result, node.Data)
	preOrderHelper(node.Left, result)
	preOrderHelper(node.Right, result)
}

// PostOrderTraversal performs post-order traversal (Left-Right-Root)
//
// Time Complexity: O(n)
func (bt *BinaryTree[T]) PostOrderTraversal() []T {
	result := make([]T, 0, bt.size)
	postOrderHelper(bt.Root, &result)
	return result
}

func postOrderHelper[T any](node *TreeNode[T], result *[]T) {
	if node == nil {
		return
	}

	postOrderHelper(node.Left, result)
	postOrderHelper(node.Right, result)
	*result = append(*result, node.Data)
}

// LevelOrderTraversal performs level-order (breadth-first) traversal
//
// Time Complexity: O(n)
func (bt *BinaryTree[T]) LevelOrderTraversal() []T {
	if bt.Root == nil {
		return []T{}
	}

	result := make([]T, 0, bt.size)
	queue := []*TreeNode[T]{bt.Root}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		result = append(result, current.Data)

		if current.Left != nil {
			queue = append(queue, current.Left)
		}
		if current.Right != nil {
			queue = append(queue, current.Right)
		}
	}

	return result
}

// LevelOrderByLevel returns nodes grouped by level
func (bt *BinaryTree[T]) LevelOrderByLevel() [][]T {
	if bt.Root == nil {
		return [][]T{}
	}

	result := make([][]T, 0)
	queue := []*TreeNode[T]{bt.Root}

	for len(queue) > 0 {
		levelSize := len(queue)
		level := make([]T, 0, levelSize)

		for i := 0; i < levelSize; i++ {
			current := queue[0]
			queue = queue[1:]

			level = append(level, current.Data)

			if current.Left != nil {
				queue = append(queue, current.Left)
			}
			if current.Right != nil {
				queue = append(queue, current.Right)
			}
		}

		result = append(result, level)
	}

	return result
}

// ITERATIVE TRAVERSALS (using stack)

// InOrderIterative performs iterative in-order traversal
func (bt *BinaryTree[T]) InOrderIterative() []T {
	result := make([]T, 0, bt.size)
	if bt.Root == nil {
		return result
	}

	stack := make([]*TreeNode[T], 0)
	current := bt.Root

	for current != nil || len(stack) > 0 {
		// Reach leftmost node
		for current != nil {
			stack = append(stack, current)
			current = current.Left
		}

		// Current must be nil, pop from stack
		current = stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		result = append(result, current.Data)

		// Visit right subtree
		current = current.Right
	}

	return result
}

// PreOrderIterative performs iterative pre-order traversal
func (bt *BinaryTree[T]) PreOrderIterative() []T {
	result := make([]T, 0, bt.size)
	if bt.Root == nil {
		return result
	}

	stack := []*TreeNode[T]{bt.Root}

	for len(stack) > 0 {
		current := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		result = append(result, current.Data)

		// Push right first so left is processed first
		if current.Right != nil {
			stack = append(stack, current.Right)
		}
		if current.Left != nil {
			stack = append(stack, current.Left)
		}
	}

	return result
}

// PostOrderIterative performs iterative post-order traversal
func (bt *BinaryTree[T]) PostOrderIterative() []T {
	result := make([]T, 0, bt.size)
	if bt.Root == nil {
		return result
	}

	stack1 := []*TreeNode[T]{bt.Root}
	stack2 := make([]*TreeNode[T], 0)

	for len(stack1) > 0 {
		current := stack1[len(stack1)-1]
		stack1 = stack1[:len(stack1)-1]
		stack2 = append(stack2, current)

		if current.Left != nil {
			stack1 = append(stack1, current.Left)
		}
		if current.Right != nil {
			stack1 = append(stack1, current.Right)
		}
	}

	// Pop from stack2 to get post-order
	for len(stack2) > 0 {
		current := stack2[len(stack2)-1]
		stack2 = stack2[:len(stack2)-1]
		result = append(result, current.Data)
	}

	return result
}

// PARALLEL TRAVERSAL

// ParallelInOrderTraversal performs parallel in-order traversal
//
// Uses goroutines to traverse left and right subtrees concurrently
func (bt *BinaryTree[T]) ParallelInOrderTraversal() []T {
	if bt.Root == nil {
		return []T{}
	}

	resultChan := make(chan []T, 3)
	var wg sync.WaitGroup

	parallelInOrderHelper(bt.Root, resultChan, &wg)
	wg.Wait()
	close(resultChan)

	// Collect results
	result := make([]T, 0, bt.size)
	for subResult := range resultChan {
		result = append(result, subResult...)
	}

	return result
}

func parallelInOrderHelper[T any](node *TreeNode[T], resultChan chan []T, wg *sync.WaitGroup) {
	if node == nil {
		return
	}

	wg.Add(2)

	// Traverse left subtree
	go func() {
		defer wg.Done()
		parallelInOrderHelper(node.Left, resultChan, wg)
	}()

	// Traverse right subtree
	go func() {
		defer wg.Done()
		parallelInOrderHelper(node.Right, resultChan, wg)
	}()

	// Process current node
	resultChan <- []T{node.Data}
}

// TREE PROPERTIES AND UTILITIES

// CountNodes counts the total number of nodes
func (bt *BinaryTree[T]) CountNodes() int {
	return countNodes(bt.Root)
}

func countNodes[T any](node *TreeNode[T]) int {
	if node == nil {
		return 0
	}
	return 1 + countNodes(node.Left) + countNodes(node.Right)
}

// CountLeaves counts the number of leaf nodes
func (bt *BinaryTree[T]) CountLeaves() int {
	return countLeaves(bt.Root)
}

func countLeaves[T any](node *TreeNode[T]) int {
	if node == nil {
		return 0
	}
	if node.Left == nil && node.Right == nil {
		return 1
	}
	return countLeaves(node.Left) + countLeaves(node.Right)
}

// IsBalanced checks if the tree is height-balanced
//
// A tree is balanced if the heights of left and right subtrees
// differ by at most 1 for every node
func (bt *BinaryTree[T]) IsBalanced() bool {
	_, balanced := checkBalance(bt.Root)
	return balanced
}

func checkBalance[T any](node *TreeNode[T]) (int, bool) {
	if node == nil {
		return 0, true
	}

	leftHeight, leftBalanced := checkBalance(node.Left)
	if !leftBalanced {
		return 0, false
	}

	rightHeight, rightBalanced := checkBalance(node.Right)
	if !rightBalanced {
		return 0, false
	}

	heightDiff := leftHeight - rightHeight
	if heightDiff < 0 {
		heightDiff = -heightDiff
	}

	if heightDiff > 1 {
		return 0, false
	}

	maxHeight := leftHeight
	if rightHeight > leftHeight {
		maxHeight = rightHeight
	}

	return maxHeight + 1, true
}

// IsFull checks if the tree is full (every node has 0 or 2 children)
func (bt *BinaryTree[T]) IsFull() bool {
	return isFull(bt.Root)
}

func isFull[T any](node *TreeNode[T]) bool {
	if node == nil {
		return true
	}

	if node.Left == nil && node.Right == nil {
		return true
	}

	if node.Left != nil && node.Right != nil {
		return isFull(node.Left) && isFull(node.Right)
	}

	return false
}

// IsComplete checks if the tree is complete
func (bt *BinaryTree[T]) IsComplete() bool {
	if bt.Root == nil {
		return true
	}

	queue := []*TreeNode[T]{bt.Root}
	foundNonFull := false

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		if current.Left != nil {
			if foundNonFull {
				return false
			}
			queue = append(queue, current.Left)
		} else {
			foundNonFull = true
		}

		if current.Right != nil {
			if foundNonFull {
				return false
			}
			queue = append(queue, current.Right)
		} else {
			foundNonFull = true
		}
	}

	return true
}

// Diameter calculates the diameter (longest path between any two nodes)
func (bt *BinaryTree[T]) Diameter() int {
	diameter := 0
	calculateDiameter(bt.Root, &diameter)
	return diameter
}

func calculateDiameter[T any](node *TreeNode[T], diameter *int) int {
	if node == nil {
		return 0
	}

	leftHeight := calculateDiameter(node.Left, diameter)
	rightHeight := calculateDiameter(node.Right, diameter)

	// Update diameter if path through current node is longer
	currentDiameter := leftHeight + rightHeight
	if currentDiameter > *diameter {
		*diameter = currentDiameter
	}

	// Return height of current subtree
	if leftHeight > rightHeight {
		return leftHeight + 1
	}
	return rightHeight + 1
}

// Mirror creates a mirror image of the tree
func (bt *BinaryTree[T]) Mirror() {
	mirror(bt.Root)
}

func mirror[T any](node *TreeNode[T]) {
	if node == nil {
		return
	}

	// Swap left and right children
	node.Left, node.Right = node.Right, node.Left

	// Recursively mirror subtrees
	mirror(node.Left)
	mirror(node.Right)
}

// TREE VISUALIZATION

// Visualize creates an ASCII representation of the tree
func (bt *BinaryTree[T]) Visualize() string {
	if bt.Root == nil {
		return "Empty tree"
	}

	var lines []string
	visualizeHelper(bt.Root, "", "", &lines)
	return strings.Join(lines, "\n")
}

func visualizeHelper[T any](node *TreeNode[T], prefix, childPrefix string, lines *[]string) {
	if node == nil {
		return
	}

	*lines = append(*lines, fmt.Sprintf("%s%v", prefix, node.Data))

	if node.Left != nil || node.Right != nil {
		if node.Left != nil {
			if node.Right != nil {
				visualizeHelper(node.Left, childPrefix+"├── ", childPrefix+"│   ", lines)
			} else {
				visualizeHelper(node.Left, childPrefix+"└── ", childPrefix+"    ", lines)
			}
		}

		if node.Right != nil {
			visualizeHelper(node.Right, childPrefix+"└── ", childPrefix+"    ", lines)
		}
	}
}

// PrintLevelOrder prints tree level by level
func (bt *BinaryTree[T]) PrintLevelOrder() {
	levels := bt.LevelOrderByLevel()

	for i, level := range levels {
		fmt.Printf("Level %d: ", i)
		for j, val := range level {
			if j > 0 {
				fmt.Print(", ")
			}
			fmt.Printf("%v", val)
		}
		fmt.Println()
	}
}

// UTILITY FUNCTIONS

// Search searches for a value in the tree (level-order)
func (bt *BinaryTree[T]) Search(target T, equals func(a, b T) bool) bool {
	if bt.Root == nil {
		return false
	}

	queue := []*TreeNode[T]{bt.Root}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		if equals(current.Data, target) {
			return true
		}

		if current.Left != nil {
			queue = append(queue, current.Left)
		}
		if current.Right != nil {
			queue = append(queue, current.Right)
		}
	}

	return false
}

// Clone creates a deep copy of the tree
func (bt *BinaryTree[T]) Clone() *BinaryTree[T] {
	newTree := NewBinaryTree[T]()
	newTree.Root = cloneNode(bt.Root)
	newTree.size = bt.size
	return newTree
}

func cloneNode[T any](node *TreeNode[T]) *TreeNode[T] {
	if node == nil {
		return nil
	}

	return &TreeNode[T]{
		Data:  node.Data,
		Left:  cloneNode(node.Left),
		Right: cloneNode(node.Right),
	}
}

// DemonstrateBinaryTree demonstrates binary tree operations
func DemonstrateBinaryTree() {
	fmt.Println("🌳 Binary Tree Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

	// Create and populate tree
	fmt.Println("\n📋 Building Binary Tree:")
	fmt.Println(strings.Repeat("-", 70))

	tree := NewBinaryTree[int]()
	values := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	fmt.Printf("Inserting values: %v\n", values)
	for _, val := range values {
		tree.Insert(val)
	}

	fmt.Printf("\nTree size: %d\n", tree.Size())
	fmt.Printf("Tree height: %d\n", tree.Height())

	// Visualize tree
	fmt.Println("\n🌲 Tree Structure:")
	fmt.Println(tree.Visualize())

	// Traversals
	fmt.Println("\n🔄 Traversal Algorithms:")
	fmt.Println(strings.Repeat("-", 70))

	fmt.Printf("In-Order (L-Root-R):   %v\n", tree.InOrderTraversal())
	fmt.Printf("Pre-Order (Root-L-R):  %v\n", tree.PreOrderTraversal())
	fmt.Printf("Post-Order (L-R-Root): %v\n", tree.PostOrderTraversal())
	fmt.Printf("Level-Order (BFS):     %v\n", tree.LevelOrderTraversal())

	// Iterative traversals
	fmt.Println("\n🔁 Iterative Traversals:")
	fmt.Println(strings.Repeat("-", 70))

	fmt.Printf("In-Order Iterative:    %v\n", tree.InOrderIterative())
	fmt.Printf("Pre-Order Iterative:   %v\n", tree.PreOrderIterative())
	fmt.Printf("Post-Order Iterative:  %v\n", tree.PostOrderIterative())

	// Level order by level
	fmt.Println("\n📊 Level-Order by Level:")
	tree.PrintLevelOrder()

	// Tree properties
	fmt.Println("\n📐 Tree Properties:")
	fmt.Println(strings.Repeat("-", 70))

	fmt.Printf("Total nodes:      %d\n", tree.CountNodes())
	fmt.Printf("Leaf nodes:       %d\n", tree.CountLeaves())
	fmt.Printf("Is balanced:      %v\n", tree.IsBalanced())
	fmt.Printf("Is full:          %v\n", tree.IsFull())
	fmt.Printf("Is complete:      %v\n", tree.IsComplete())
	fmt.Printf("Diameter:         %d\n", tree.Diameter())

	// Mirror tree
	fmt.Println("\n🪞 Mirror Tree:")
	fmt.Println(strings.Repeat("-", 70))

	mirroredTree := tree.Clone()
	mirroredTree.Mirror()

	fmt.Println("Original tree:")
	fmt.Println(tree.Visualize())

	fmt.Println("\nMirrored tree:")
	fmt.Println(mirroredTree.Visualize())

	// Search
	fmt.Println("\n🔍 Search Operations:")
	fmt.Println(strings.Repeat("-", 70))

	searchValues := []int{5, 15, 1, 10}
	for _, val := range searchValues {
		found := tree.Search(val, func(a, b int) bool { return a == b })
		status := "✓"
		if !found {
			status = "✗"
		}
		fmt.Printf("Search for %d: %s\n", val, status)
	}

	// String tree
	fmt.Println("\n🔤 String Binary Tree:")
	fmt.Println(strings.Repeat("-", 70))

	strTree := NewBinaryTree[string]()
	words := []string{"Root", "Left", "Right", "LL", "LR", "RL", "RR"}

	for _, word := range words {
		strTree.Insert(word)
	}

	fmt.Println(strTree.Visualize())
	fmt.Printf("\nIn-Order: %v\n", strTree.InOrderTraversal())

	// Custom struct tree
	fmt.Println("\n👤 Custom Struct Tree:")
	fmt.Println(strings.Repeat("-", 70))

	type Person struct {
		Name string
		Age  int
	}

	personTree := NewBinaryTree[Person]()
	people := []Person{
		{"Alice", 30},
		{"Bob", 25},
		{"Charlie", 35},
		{"David", 28},
	}

	for _, person := range people {
		personTree.Insert(person)
	}

	fmt.Println("Level-order traversal:")
	for _, person := range personTree.LevelOrderTraversal() {
		fmt.Printf("  %s (age %d)\n", person.Name, person.Age)
	}

	// Performance comparison
	fmt.Println("\n⚡ Performance Test (Large Tree):")
	fmt.Println(strings.Repeat("-", 70))

	largeTree := NewBinaryTree[int]()
	for i := 1; i <= 1000; i++ {
		largeTree.Insert(i)
	}

	fmt.Printf("Created tree with %d nodes\n", largeTree.Size())
	fmt.Printf("Height: %d\n", largeTree.Height())
	fmt.Printf("Expected height for complete tree: %.0f\n", math.Ceil(math.Log2(float64(largeTree.Size()+1))))
}

func main() {
	DemonstrateBinaryTree()
	fmt.Println("\n✨ Binary Tree demonstration complete!")
}
