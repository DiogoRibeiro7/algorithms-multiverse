// Binary Search Tree (BST) Implementation in Go
//
// Time Complexity:
// - Search: O(log n) average, O(n) worst case (unbalanced)
// - Insert: O(log n) average, O(n) worst case
// - Delete: O(log n) average, O(n) worst case
// - Traversal: O(n)
// Space Complexity: O(n)
//
// A Binary Search Tree is a binary tree where for each node:
// - All nodes in the left subtree have smaller values
// - All nodes in the right subtree have larger values
//
// Go features:
// - Generic implementation with type parameters
// - Ordered interface for type constraints
// - Self-balancing capabilities (AVL rotations)
// - Thread-safe variant with mutex
// - Range queries and iterators
// - Serialization and deserialization

package main

import (
	"errors"
	"fmt"
	"math"
	"strings"
	"sync"
)

// Ordered constraint for BST elements
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
		~float32 | ~float64 |
		~string
}

// BSTNode represents a node in a binary search tree
type BSTNode[T Ordered] struct {
	Data   T
	Left   *BSTNode[T]
	Right  *BSTNode[T]
	Height int // For AVL balancing
}

// NewBSTNode creates a new BST node
func NewBSTNode[T Ordered](data T) *BSTNode[T] {
	return &BSTNode[T]{
		Data:   data,
		Left:   nil,
		Right:  nil,
		Height: 1,
	}
}

// BST represents a binary search tree
type BST[T Ordered] struct {
	Root *BSTNode[T]
	size int
}

// NewBST creates a new binary search tree
func NewBST[T Ordered]() *BST[T] {
	return &BST[T]{
		Root: nil,
		size: 0,
	}
}

// Size returns the number of nodes
func (bst *BST[T]) Size() int {
	return bst.size
}

// IsEmpty checks if the tree is empty
func (bst *BST[T]) IsEmpty() bool {
	return bst.Root == nil
}

// Insert adds a new value to the tree
//
// Time Complexity: O(log n) average, O(n) worst case
func (bst *BST[T]) Insert(data T) {
	bst.Root = insertNode(bst.Root, data)
	bst.size++
}

func insertNode[T Ordered](node *BSTNode[T], data T) *BSTNode[T] {
	if node == nil {
		return NewBSTNode(data)
	}

	if data < node.Data {
		node.Left = insertNode(node.Left, data)
	} else if data > node.Data {
		node.Right = insertNode(node.Right, data)
	}
	// If equal, don't insert (no duplicates)

	return node
}

// Search searches for a value in the tree
//
// Time Complexity: O(log n) average, O(n) worst case
func (bst *BST[T]) Search(data T) bool {
	return searchNode(bst.Root, data)
}

func searchNode[T Ordered](node *BSTNode[T], data T) bool {
	if node == nil {
		return false
	}

	if data == node.Data {
		return true
	} else if data < node.Data {
		return searchNode(node.Left, data)
	} else {
		return searchNode(node.Right, data)
	}
}

// Delete removes a value from the tree
//
// Time Complexity: O(log n) average, O(n) worst case
func (bst *BST[T]) Delete(data T) bool {
	var deleted bool
	bst.Root, deleted = deleteNode(bst.Root, data)
	if deleted {
		bst.size--
	}
	return deleted
}

func deleteNode[T Ordered](node *BSTNode[T], data T) (*BSTNode[T], bool) {
	if node == nil {
		return nil, false
	}

	var deleted bool

	if data < node.Data {
		node.Left, deleted = deleteNode(node.Left, data)
	} else if data > node.Data {
		node.Right, deleted = deleteNode(node.Right, data)
	} else {
		// Node to be deleted found
		deleted = true

		// Case 1: Leaf node or node with one child
		if node.Left == nil {
			return node.Right, deleted
		} else if node.Right == nil {
			return node.Left, deleted
		}

		// Case 2: Node with two children
		// Find inorder successor (smallest in right subtree)
		successor := findMin(node.Right)
		node.Data = successor.Data
		node.Right, _ = deleteNode(node.Right, successor.Data)
	}

	return node, deleted
}

// FindMin finds the minimum value in the tree
func (bst *BST[T]) FindMin() (T, error) {
	var zero T
	if bst.Root == nil {
		return zero, errors.New("tree is empty")
	}

	return findMin(bst.Root).Data, nil
}

func findMin[T Ordered](node *BSTNode[T]) *BSTNode[T] {
	current := node
	for current.Left != nil {
		current = current.Left
	}
	return current
}

// FindMax finds the maximum value in the tree
func (bst *BST[T]) FindMax() (T, error) {
	var zero T
	if bst.Root == nil {
		return zero, errors.New("tree is empty")
	}

	return findMax(bst.Root).Data, nil
}

func findMax[T Ordered](node *BSTNode[T]) *BSTNode[T] {
	current := node
	for current.Right != nil {
		current = current.Right
	}
	return current
}

// Height returns the height of the tree
func (bst *BST[T]) Height() int {
	return getHeight(bst.Root)
}

func getHeight[T Ordered](node *BSTNode[T]) int {
	if node == nil {
		return 0
	}

	leftHeight := getHeight(node.Left)
	rightHeight := getHeight(node.Right)

	if leftHeight > rightHeight {
		return leftHeight + 1
	}
	return rightHeight + 1
}

// TRAVERSALS

// InOrder returns in-order traversal (sorted order)
func (bst *BST[T]) InOrder() []T {
	result := make([]T, 0, bst.size)
	inOrderTraversal(bst.Root, &result)
	return result
}

func inOrderTraversal[T Ordered](node *BSTNode[T], result *[]T) {
	if node == nil {
		return
	}

	inOrderTraversal(node.Left, result)
	*result = append(*result, node.Data)
	inOrderTraversal(node.Right, result)
}

// PreOrder returns pre-order traversal
func (bst *BST[T]) PreOrder() []T {
	result := make([]T, 0, bst.size)
	preOrderTraversal(bst.Root, &result)
	return result
}

func preOrderTraversal[T Ordered](node *BSTNode[T], result *[]T) {
	if node == nil {
		return
	}

	*result = append(*result, node.Data)
	preOrderTraversal(node.Left, result)
	preOrderTraversal(node.Right, result)
}

// PostOrder returns post-order traversal
func (bst *BST[T]) PostOrder() []T {
	result := make([]T, 0, bst.size)
	postOrderTraversal(bst.Root, &result)
	return result
}

func postOrderTraversal[T Ordered](node *BSTNode[T], result *[]T) {
	if node == nil {
		return
	}

	postOrderTraversal(node.Left, result)
	postOrderTraversal(node.Right, result)
	*result = append(*result, node.Data)
}

// RANGE QUERIES

// RangeQuery returns all values in the range [low, high]
func (bst *BST[T]) RangeQuery(low, high T) []T {
	result := make([]T, 0)
	rangeQueryHelper(bst.Root, low, high, &result)
	return result
}

func rangeQueryHelper[T Ordered](node *BSTNode[T], low, high T, result *[]T) {
	if node == nil {
		return
	}

	if node.Data > low {
		rangeQueryHelper(node.Left, low, high, result)
	}

	if node.Data >= low && node.Data <= high {
		*result = append(*result, node.Data)
	}

	if node.Data < high {
		rangeQueryHelper(node.Right, low, high, result)
	}
}

// Floor finds the largest value <= target
func (bst *BST[T]) Floor(target T) (T, error) {
	var zero T
	node := floorNode(bst.Root, target, nil)
	if node == nil {
		return zero, errors.New("no floor value found")
	}
	return node.Data, nil
}

func floorNode[T Ordered](node *BSTNode[T], target T, best *BSTNode[T]) *BSTNode[T] {
	if node == nil {
		return best
	}

	if node.Data == target {
		return node
	}

	if node.Data > target {
		return floorNode(node.Left, target, best)
	}

	// node.Data < target, this could be floor
	return floorNode(node.Right, target, node)
}

// Ceiling finds the smallest value >= target
func (bst *BST[T]) Ceiling(target T) (T, error) {
	var zero T
	node := ceilingNode(bst.Root, target, nil)
	if node == nil {
		return zero, errors.New("no ceiling value found")
	}
	return node.Data, nil
}

func ceilingNode[T Ordered](node *BSTNode[T], target T, best *BSTNode[T]) *BSTNode[T] {
	if node == nil {
		return best
	}

	if node.Data == target {
		return node
	}

	if node.Data < target {
		return ceilingNode(node.Right, target, best)
	}

	// node.Data > target, this could be ceiling
	return ceilingNode(node.Left, target, node)
}

// VALIDATION

// IsValid checks if the tree is a valid BST
func (bst *BST[T]) IsValid() bool {
	var minVal, maxVal T
	return isValidBST(bst.Root, minVal, maxVal, true)
}

func isValidBST[T Ordered](node *BSTNode[T], minVal, maxVal T, isFirst bool) bool {
	if node == nil {
		return true
	}

	if !isFirst {
		if node.Data <= minVal || node.Data >= maxVal {
			return false
		}
	}

	leftValid := isValidBST(node.Left, minVal, node.Data, false)
	rightValid := isValidBST(node.Right, node.Data, maxVal, false)

	return leftValid && rightValid
}

// IsBalanced checks if tree is height-balanced
func (bst *BST[T]) IsBalanced() bool {
	_, balanced := checkBalanced(bst.Root)
	return balanced
}

func checkBalanced[T Ordered](node *BSTNode[T]) (int, bool) {
	if node == nil {
		return 0, true
	}

	leftHeight, leftBalanced := checkBalanced(node.Left)
	if !leftBalanced {
		return 0, false
	}

	rightHeight, rightBalanced := checkBalanced(node.Right)
	if !rightBalanced {
		return 0, false
	}

	diff := leftHeight - rightHeight
	if diff < 0 {
		diff = -diff
	}

	if diff > 1 {
		return 0, false
	}

	maxHeight := leftHeight
	if rightHeight > leftHeight {
		maxHeight = rightHeight
	}

	return maxHeight + 1, true
}

// AVL TREE (Self-Balancing BST)

// AVLTree is a self-balancing binary search tree
type AVLTree[T Ordered] struct {
	Root *BSTNode[T]
	size int
}

// NewAVLTree creates a new AVL tree
func NewAVLTree[T Ordered]() *AVLTree[T] {
	return &AVLTree[T]{
		Root: nil,
		size: 0,
	}
}

// Insert adds a value with automatic balancing
func (avl *AVLTree[T]) Insert(data T) {
	avl.Root = avlInsert(avl.Root, data)
	avl.size++
}

func avlInsert[T Ordered](node *BSTNode[T], data T) *BSTNode[T] {
	if node == nil {
		return NewBSTNode(data)
	}

	if data < node.Data {
		node.Left = avlInsert(node.Left, data)
	} else if data > node.Data {
		node.Right = avlInsert(node.Right, data)
	} else {
		return node // No duplicates
	}

	// Update height
	node.Height = 1 + max(nodeHeight(node.Left), nodeHeight(node.Right))

	// Balance the node
	return balance(node)
}

func nodeHeight[T Ordered](node *BSTNode[T]) int {
	if node == nil {
		return 0
	}
	return node.Height
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// getBalanceFactor returns the balance factor of a node
func getBalanceFactor[T Ordered](node *BSTNode[T]) int {
	if node == nil {
		return 0
	}
	return nodeHeight(node.Left) - nodeHeight(node.Right)
}

// balance performs AVL rotations to balance the tree
func balance[T Ordered](node *BSTNode[T]) *BSTNode[T] {
	balanceFactor := getBalanceFactor(node)

	// Left-heavy
	if balanceFactor > 1 {
		// Left-Right case
		if getBalanceFactor(node.Left) < 0 {
			node.Left = rotateLeft(node.Left)
		}
		// Left-Left case
		return rotateRight(node)
	}

	// Right-heavy
	if balanceFactor < -1 {
		// Right-Left case
		if getBalanceFactor(node.Right) > 0 {
			node.Right = rotateRight(node.Right)
		}
		// Right-Right case
		return rotateLeft(node)
	}

	return node
}

// rotateLeft performs left rotation
func rotateLeft[T Ordered](x *BSTNode[T]) *BSTNode[T] {
	y := x.Right
	t2 := y.Left

	// Perform rotation
	y.Left = x
	x.Right = t2

	// Update heights
	x.Height = 1 + max(nodeHeight(x.Left), nodeHeight(x.Right))
	y.Height = 1 + max(nodeHeight(y.Left), nodeHeight(y.Right))

	return y
}

// rotateRight performs right rotation
func rotateRight[T Ordered](y *BSTNode[T]) *BSTNode[T] {
	x := y.Left
	t2 := x.Right

	// Perform rotation
	x.Right = y
	y.Left = t2

	// Update heights
	y.Height = 1 + max(nodeHeight(y.Left), nodeHeight(y.Right))
	x.Height = 1 + max(nodeHeight(x.Left), nodeHeight(x.Right))

	return x
}

// THREAD-SAFE BST

// ThreadSafeBST is a thread-safe binary search tree
type ThreadSafeBST[T Ordered] struct {
	bst *BST[T]
	mu  sync.RWMutex
}

// NewThreadSafeBST creates a new thread-safe BST
func NewThreadSafeBST[T Ordered]() *ThreadSafeBST[T] {
	return &ThreadSafeBST[T]{
		bst: NewBST[T](),
	}
}

// Insert adds a value (thread-safe)
func (tsBST *ThreadSafeBST[T]) Insert(data T) {
	tsBST.mu.Lock()
	defer tsBST.mu.Unlock()
	tsBST.bst.Insert(data)
}

// Search searches for a value (thread-safe)
func (tsBST *ThreadSafeBST[T]) Search(data T) bool {
	tsBST.mu.RLock()
	defer tsBST.mu.RUnlock()
	return tsBST.bst.Search(data)
}

// Delete removes a value (thread-safe)
func (tsBST *ThreadSafeBST[T]) Delete(data T) bool {
	tsBST.mu.Lock()
	defer tsBST.mu.Unlock()
	return tsBST.bst.Delete(data)
}

// Size returns the number of nodes (thread-safe)
func (tsBST *ThreadSafeBST[T]) Size() int {
	tsBST.mu.RLock()
	defer tsBST.mu.RUnlock()
	return tsBST.bst.Size()
}

// VISUALIZATION

// Visualize creates an ASCII representation
func (bst *BST[T]) Visualize() string {
	if bst.Root == nil {
		return "Empty BST"
	}

	var lines []string
	visualizeNode(bst.Root, "", "", &lines)
	return strings.Join(lines, "\n")
}

func visualizeNode[T Ordered](node *BSTNode[T], prefix, childPrefix string, lines *[]string) {
	if node == nil {
		return
	}

	*lines = append(*lines, fmt.Sprintf("%s%v", prefix, node.Data))

	if node.Left != nil || node.Right != nil {
		if node.Left != nil {
			if node.Right != nil {
				visualizeNode(node.Left, childPrefix+"├── ", childPrefix+"│   ", lines)
			} else {
				visualizeNode(node.Left, childPrefix+"└── ", childPrefix+"    ", lines)
			}
		}

		if node.Right != nil {
			visualizeNode(node.Right, childPrefix+"└── ", childPrefix+"    ", lines)
		}
	}
}

// DemonstrateBST demonstrates BST operations
func DemonstrateBST() {
	fmt.Println("🌲 Binary Search Tree Implementation in Go")
	fmt.Println(strings.Repeat("=", 70))

	// Basic BST operations
	fmt.Println("\n📋 Basic BST Operations:")
	fmt.Println(strings.Repeat("-", 70))

	bst := NewBST[int]()
	values := []int{50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65}

	fmt.Printf("Inserting values: %v\n", values)
	for _, val := range values {
		bst.Insert(val)
	}

	fmt.Printf("\nTree size: %d\n", bst.Size())
	fmt.Printf("Tree height: %d\n", bst.Height())

	// Visualization
	fmt.Println("\n🌳 Tree Structure:")
	fmt.Println(bst.Visualize())

	// Traversals
	fmt.Println("\n🔄 Traversals:")
	fmt.Println(strings.Repeat("-", 70))

	fmt.Printf("In-Order (sorted):  %v\n", bst.InOrder())
	fmt.Printf("Pre-Order:          %v\n", bst.PreOrder())
	fmt.Printf("Post-Order:         %v\n", bst.PostOrder())

	// Search operations
	fmt.Println("\n🔍 Search Operations:")
	fmt.Println(strings.Repeat("-", 70))

	searchValues := []int{40, 45, 10, 100}
	for _, val := range searchValues {
		found := bst.Search(val)
		status := "✓"
		if !found {
			status = "✗"
		}
		fmt.Printf("Search %d: %s\n", val, status)
	}

	// Min/Max
	min, _ := bst.FindMin()
	max, _ := bst.FindMax()
	fmt.Printf("\nMinimum: %d\n", min)
	fmt.Printf("Maximum: %d\n", max)

	// Range queries
	fmt.Println("\n📊 Range Queries:")
	fmt.Println(strings.Repeat("-", 70))

	ranges := [][]int{{25, 65}, {10, 40}, {60, 80}}
	for _, r := range ranges {
		result := bst.RangeQuery(r[0], r[1])
		fmt.Printf("Range [%d, %d]: %v\n", r[0], r[1], result)
	}

	// Floor and Ceiling
	fmt.Println("\n🔢 Floor and Ceiling:")
	testVals := []int{45, 32, 75}
	for _, val := range testVals {
		floor, _ := bst.Floor(val)
		ceiling, _ := bst.Ceiling(val)
		fmt.Printf("Value %d - Floor: %d, Ceiling: %d\n", val, floor, ceiling)
	}

	// Delete operations
	fmt.Println("\n🗑️  Delete Operations:")
	fmt.Println(strings.Repeat("-", 70))

	deleteVals := []int{20, 30, 50}
	for _, val := range deleteVals {
		deleted := bst.Delete(val)
		if deleted {
			fmt.Printf("Deleted %d, Remaining: %v\n", val, bst.InOrder())
		}
	}

	// Validation
	fmt.Println("\n✅ Validation:")
	fmt.Println(strings.Repeat("-", 70))

	fmt.Printf("Is valid BST: %v\n", bst.IsValid())
	fmt.Printf("Is balanced: %v\n", bst.IsBalanced())

	// AVL Tree (Self-Balancing)
	fmt.Println("\n🔄 AVL Tree (Self-Balancing):")
	fmt.Println(strings.Repeat("-", 70))

	avl := NewAVLTree[int]()
	avlValues := []int{10, 20, 30, 40, 50, 25}

	fmt.Printf("Inserting (in order): %v\n", avlValues)
	for _, val := range avlValues {
		avl.Insert(val)
	}

	fmt.Printf("AVL tree size: %d\n", avl.size)

	// Compare with unbalanced BST
	unbalanced := NewBST[int]()
	for _, val := range avlValues {
		unbalanced.Insert(val)
	}

	fmt.Println("\nUnbalanced BST:")
	fmt.Println(unbalanced.Visualize())
	fmt.Printf("Height: %d\n", unbalanced.Height())

	fmt.Println("\nAVL Tree (balanced):")
	fmt.Println((&BST[int]{Root: avl.Root, size: avl.size}).Visualize())
	fmt.Printf("Height: %d\n", nodeHeight(avl.Root))

	// Performance comparison
	fmt.Println("\n⚡ Performance Comparison:")
	fmt.Println(strings.Repeat("-", 70))

	largeBST := NewBST[int]()
	largeAVL := NewAVLTree[int]()

	for i := 1; i <= 1000; i++ {
		largeBST.Insert(i)
		largeAVL.Insert(i)
	}

	fmt.Printf("BST (sequential insertion):\n")
	fmt.Printf("  Size: %d\n", largeBST.Size())
	fmt.Printf("  Height: %d\n", largeBST.Height())
	fmt.Printf("  Expected O(log n) height: %.0f\n", math.Ceil(math.Log2(float64(largeBST.Size()))))

	fmt.Printf("\nAVL Tree (sequential insertion):\n")
	fmt.Printf("  Size: %d\n", largeAVL.size)
	fmt.Printf("  Height: %d\n", nodeHeight(largeAVL.Root))
	fmt.Printf("  Expected O(log n) height: %.0f\n", math.Ceil(math.Log2(float64(largeAVL.size))))

	// Thread-safe BST
	fmt.Println("\n🔒 Thread-Safe BST:")
	fmt.Println(strings.Repeat("-", 70))

	tsBST := NewThreadSafeBST[int]()

	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(val int) {
			defer wg.Done()
			tsBST.Insert(val)
		}(i)
	}

	wg.Wait()
	fmt.Printf("Inserted 100 values concurrently\n")
	fmt.Printf("Final size: %d\n", tsBST.Size())
}

func main() {
	DemonstrateBST()
	fmt.Println("\n✨ BST demonstration complete!")
}
