/*
 * ==============================================================================
 * Tree Data Structures in Swift
 *
 * Binary search trees and self-balancing variants using Swift's
 * class-based reference semantics for tree nodes.
 *
 * Implementations:
 * - Binary Search Tree (BST)
 * - AVL Tree (self-balancing)
 * - Tree Traversals (inorder, preorder, postorder, level-order)
 *
 * Swift's class references make tree manipulation natural and efficient.
 *
 * Compile: swiftc -O trees.swift
 * Run: ./trees
 *
 * @author Algorithms Multiverse
 * @version 1.0
 * ==============================================================================
 */

import Foundation

// ==============================================================================
// Tree Node (Reference Type)
// ==============================================================================

class TreeNode {
    var value: Int
    var left: TreeNode?
    var right: TreeNode?
    var height: Int = 1  // For AVL trees

    init(_ value: Int) {
        self.value = value
    }
}

// ==============================================================================
// Binary Search Tree Operations
// ==============================================================================

/// Insert into BST
///
/// Time Complexity: O(h) where h = height
func bstInsert(_ root: TreeNode?, _ value: Int) -> TreeNode {
    guard let root = root else {
        return TreeNode(value)
    }

    if value < root.value {
        root.left = bstInsert(root.left, value)
    } else if value > root.value {
        root.right = bstInsert(root.right, value)
    }

    return root
}

/// Search in BST
///
/// Time Complexity: O(h)
func bstSearch(_ root: TreeNode?, _ value: Int) -> Bool {
    guard let root = root else { return false }

    if root.value == value {
        return true
    } else if value < root.value {
        return bstSearch(root.left, value)
    } else {
        return bstSearch(root.right, value)
    }
}

/// Find Minimum Value
func bstFindMin(_ root: TreeNode?) -> Int? {
    guard let root = root else { return nil }
    var current = root
    while let left = current.left {
        current = left
    }
    return current.value
}

/// Delete from BST
func bstDelete(_ root: TreeNode?, _ value: Int) -> TreeNode? {
    guard let root = root else { return nil }

    if value < root.value {
        root.left = bstDelete(root.left, value)
    } else if value > root.value {
        root.right = bstDelete(root.right, value)
    } else {
        // Node found
        if root.left == nil {
            return root.right
        } else if root.right == nil {
            return root.left
        }

        // Two children: find inorder successor
        if let minValue = bstFindMin(root.right) {
            root.value = minValue
            root.right = bstDelete(root.right, minValue)
        }
    }

    return root
}

// ==============================================================================
// Tree Traversals
// ==============================================================================

/// Inorder Traversal (Left, Root, Right)
func inorderTraversal(_ root: TreeNode?) -> [Int] {
    guard let root = root else { return [] }
    return inorderTraversal(root.left) + [root.value] + inorderTraversal(root.right)
}

/// Preorder Traversal (Root, Left, Right)
func preorderTraversal(_ root: TreeNode?) -> [Int] {
    guard let root = root else { return [] }
    return [root.value] + preorderTraversal(root.left) + preorderTraversal(root.right)
}

/// Postorder Traversal (Left, Right, Root)
func postorderTraversal(_ root: TreeNode?) -> [Int] {
    guard let root = root else { return [] }
    return postorderTraversal(root.left) + postorderTraversal(root.right) + [root.value]
}

/// Level-order Traversal (BFS)
func levelorderTraversal(_ root: TreeNode?) -> [Int] {
    guard let root = root else { return [] }

    var result = [Int]()
    var queue = [root]

    while !queue.isEmpty {
        let node = queue.removeFirst()
        result.append(node.value)

        if let left = node.left { queue.append(left) }
        if let right = node.right { queue.append(right) }
    }

    return result
}

/// Tree Height
func treeHeight(_ root: TreeNode?) -> Int {
    guard let root = root else { return 0 }
    return 1 + max(treeHeight(root.left), treeHeight(root.right))
}

// ==============================================================================
// AVL Tree (Self-Balancing BST)
// ==============================================================================

func getHeight(_ node: TreeNode?) -> Int {
    return node?.height ?? 0
}

func getBalance(_ node: TreeNode?) -> Int {
    guard let node = node else { return 0 }
    return getHeight(node.left) - getHeight(node.right)
}

func rightRotate(_ y: TreeNode) -> TreeNode {
    let x = y.left!
    let T2 = x.right

    x.right = y
    y.left = T2

    y.height = max(getHeight(y.left), getHeight(y.right)) + 1
    x.height = max(getHeight(x.left), getHeight(x.right)) + 1

    return x
}

func leftRotate(_ x: TreeNode) -> TreeNode {
    let y = x.right!
    let T2 = y.left

    y.left = x
    x.right = T2

    x.height = max(getHeight(x.left), getHeight(x.right)) + 1
    y.height = max(getHeight(y.left), getHeight(y.right)) + 1

    return y
}

/// Insert into AVL Tree
///
/// Time Complexity: O(log n) - guaranteed balanced
func avlInsert(_ root: TreeNode?, _ value: Int) -> TreeNode {
    // Standard BST insert
    guard let root = root else {
        return TreeNode(value)
    }

    if value < root.value {
        root.left = avlInsert(root.left, value)
    } else if value > root.value {
        root.right = avlInsert(root.right, value)
    } else {
        return root  // Duplicates not allowed
    }

    // Update height
    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    // Get balance factor
    let balance = getBalance(root)

    // Left Left Case
    if balance > 1 && value < root.left!.value {
        return rightRotate(root)
    }

    // Right Right Case
    if balance < -1 && value > root.right!.value {
        return leftRotate(root)
    }

    // Left Right Case
    if balance > 1 && value > root.left!.value {
        root.left = leftRotate(root.left!)
        return rightRotate(root)
    }

    // Right Left Case
    if balance < -1 && value < root.right!.value {
        root.right = rightRotate(root.right!)
        return leftRotate(root)
    }

    return root
}

// ==============================================================================
// Main Program - Examples and Tests
// ==============================================================================

print("==============================================================================")
print("                TREE DATA STRUCTURES IN SWIFT")
print("       Binary Search Trees & Self-Balancing AVL Trees")
print("==============================================================================\n")

// Example 1: BST Operations
print("Example 1: Binary Search Tree (BST)")
print(String(repeating: "=", count: 80))

var bstRoot: TreeNode? = nil
let values = [50, 30, 70, 20, 40, 60, 80]

print("Inserting:", values.map { String($0) }.joined(separator: ", "))
for value in values {
    bstRoot = bstInsert(bstRoot, value)
}

print("Inorder (sorted):", inorderTraversal(bstRoot).map { String($0) }.joined(separator: ", "))
print("Preorder:", preorderTraversal(bstRoot).map { String($0) }.joined(separator: ", "))
print("Postorder:", postorderTraversal(bstRoot).map { String($0) }.joined(separator: ", "))
print("Level-order:", levelorderTraversal(bstRoot).map { String($0) }.joined(separator: ", "))
print("Tree height:", treeHeight(bstRoot))

print("\nSearch 40:", bstSearch(bstRoot, 40))
print("Search 100:", bstSearch(bstRoot, 100))

print("\nDeleting 30...")
bstRoot = bstDelete(bstRoot, 30)
print("Inorder after delete:", inorderTraversal(bstRoot).map { String($0) }.joined(separator: ", "))
print()

// Example 2: AVL Tree
print("Example 2: AVL Tree (Self-Balancing BST)")
print(String(repeating: "=", count: 80))

var avlRoot: TreeNode? = nil
let avlValues = [10, 20, 30, 40, 50, 25]

print("Inserting:", avlValues.map { String($0) }.joined(separator: ", "))
for value in avlValues {
    avlRoot = avlInsert(avlRoot, value)
}

print("Inorder:", inorderTraversal(avlRoot).map { String($0) }.joined(separator: ", "))
print("Tree height:", treeHeight(avlRoot), "(balanced!)")
print("Balance factor at root:", getBalance(avlRoot))
print()

// Example 3: Comparison BST vs AVL
print("Example 3: Comparison - BST vs AVL (Worst Case)")
print(String(repeating: "=", count: 80))

let sortedValues = Array(1...100)

print("Inserting sorted values 1-100:\n")

// Regular BST
var bstRoot2: TreeNode? = nil
for value in sortedValues {
    bstRoot2 = bstInsert(bstRoot2, value)
}
print("Regular BST height:", treeHeight(bstRoot2), "(degenerate - like linked list!)")

// AVL Tree
var avlRoot2: TreeNode? = nil
for value in sortedValues {
    avlRoot2 = avlInsert(avlRoot2, value)
}
print("AVL Tree height:", treeHeight(avlRoot2), "(balanced - O(log n))")
print()

// Summary
print(String(repeating: "=", count: 80))
print("Summary: Tree Data Structures in Swift")
print(String(repeating: "=", count: 80))
print("✓ BST: O(log n) average, O(n) worst case")
print("✓ AVL: O(log n) guaranteed (self-balancing)")
print("✓ Traversals: Inorder, Preorder, Postorder, Level-order")
print("\nSwift Advantages:")
print("- Reference semantics for tree nodes")
print("- Optional types for null safety")
print("- Class-based inheritance")
print("\nApplications:")
print("- Databases (indexing)")
print("- File systems")
print("- Priority queues")
print("- Symbol tables")
print(String(repeating: "=", count: 80))
