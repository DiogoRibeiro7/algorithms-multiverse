/**
 * Binary Tree Implementation in JavaScript
 * 
 * Time Complexity:
 * - Insert: O(log n) average, O(n) worst case
 * - Search: O(log n) average, O(n) worst case
 * - Delete: O(log n) average, O(n) worst case
 * 
 * Space Complexity: O(n) for storage, O(log n) for recursion stack
 * 
 * JavaScript features:
 * - ES6+ syntax
 * - Generator functions
 * - Classes and modules
 * - Async/await support
 */

class TreeNode {
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
    }
    
    toString() {
        return this.data.toString();
    }
}

class BinaryTree {
    constructor() {
        this.root = null;
        this.size = 0;
    }
    
    // Core Operations
    
    insert(data) {
        if (this.root === null) {
            this.root = new TreeNode(data);
        } else {
            this._insertRecursive(this.root, data);
        }
        this.size++;
        return this;
    }
    
    _insertRecursive(node, data) {
        if (data < node.data) {
            if (node.left === null) {
                node.left = new TreeNode(data);
            } else {
                this._insertRecursive(node.left, data);
            }
        } else {
            if (node.right === null) {
                node.right = new TreeNode(data);
            } else {
                this._insertRecursive(node.right, data);
            }
        }
    }
    
    search(data) {
        return this._searchRecursive(this.root, data);
    }
    
    _searchRecursive(node, data) {
        if (node === null) {
            return false;
        }
        
        if (data === node.data) {
            return true;
        } else if (data < node.data) {
            return this._searchRecursive(node.left, data);
        } else {
            return this._searchRecursive(node.right, data);
        }
    }
    
    delete(data) {
        if (this.root === null) {
            return false;
        }
        
        const result = this._deleteRecursive(this.root, data);
        this.root = result.node;
        
        if (result.deleted) {
            this.size--;
        }
        
        return result.deleted;
    }
    
    _deleteRecursive(node, data) {
        if (node === null) {
            return { node: null, deleted: false };
        }
        
        if (data < node.data) {
            const result = this._deleteRecursive(node.left, data);
            node.left = result.node;
            return { node, deleted: result.deleted };
        } else if (data > node.data) {
            const result = this._deleteRecursive(node.right, data);
            node.right = result.node;
            return { node, deleted: result.deleted };
        } else {
            // Node to delete found
            if (node.left === null) {
                return { node: node.right, deleted: true };
            } else if (node.right === null) {
                return { node: node.left, deleted: true };
            } else {
                // Node has two children
                const minNode = this._findMin(node.right);
                node.data = minNode.data;
                const result = this._deleteRecursive(node.right, minNode.data);
                node.right = result.node;
                return { node, deleted: true };
            }
        }
    }
    
    _findMin(node) {
        while (node.left !== null) {
            node = node.left;
        }
        return node;
    }
    
    _findMax(node) {
        while (node.right !== null) {
            node = node.right;
        }
        return node;
    }
    
    // Traversal Methods (Using Generators)
    
    *inorderTraversal(node = this.root) {
        if (node !== null) {
            yield* this.inorderTraversal(node.left);
            yield node.data;
            yield* this.inorderTraversal(node.right);
        }
    }
    
    *preorderTraversal(node = this.root) {
        if (node !== null) {
            yield node.data;
            yield* this.preorderTraversal(node.left);
            yield* this.preorderTraversal(node.right);
        }
    }
    
    *postorderTraversal(node = this.root) {
        if (node !== null) {
            yield* this.postorderTraversal(node.left);
            yield* this.postorderTraversal(node.right);
            yield node.data;
        }
    }
    
    *levelOrderTraversal() {
        if (this.root === null) return;
        
        const queue = [this.root];
        while (queue.length > 0) {
            const node = queue.shift();
            yield node.data;
            
            if (node.left !== null) {
                queue.push(node.left);
            }
            if (node.right !== null) {
                queue.push(node.right);
            }
        }
    }
    
    // Utility Methods
    
    height(node = this.root) {
        if (node === null) {
            return -1;
        }
        
        const leftHeight = this.height(node.left);
        const rightHeight = this.height(node.right);
        
        return 1 + Math.max(leftHeight, rightHeight);
    }
    
    depth(data, node = this.root, currentDepth = 0) {
        if (node === null) {
            return -1;
        }
        
        if (node.data === data) {
            return currentDepth;
        }
        
        if (data < node.data) {
            return this.depth(data, node.left, currentDepth + 1);
        } else {
            return this.depth(data, node.right, currentDepth + 1);
        }
    }
    
    isBalanced(node = this.root) {
        const result = this._isBalancedRecursive(node);
        return result.balanced;
    }
    
    _isBalancedRecursive(node) {
        if (node === null) {
            return { balanced: true, height: -1 };
        }
        
        const leftResult = this._isBalancedRecursive(node.left);
        const rightResult = this._isBalancedRecursive(node.right);
        
        const balanced = leftResult.balanced && 
                        rightResult.balanced && 
                        Math.abs(leftResult.height - rightResult.height) <= 1;
        
        const height = 1 + Math.max(leftResult.height, rightResult.height);
        
        return { balanced, height };
    }
    
    countNodes() {
        return this.size;
    }
    
    countLeaves(node = this.root) {
        if (node === null) {
            return 0;
        }
        
        if (node.left === null && node.right === null) {
            return 1;
        }
        
        return this.countLeaves(node.left) + this.countLeaves(node.right);
    }
    
    getLevelNodes(targetLevel, node = this.root, currentLevel = 0) {
        if (node === null) {
            return [];
        }
        
        if (currentLevel === targetLevel) {
            return [node.data];
        }
        
        return [
            ...this.getLevelNodes(targetLevel, node.left, currentLevel + 1),
            ...this.getLevelNodes(targetLevel, node.right, currentLevel + 1)
        ];
    }
    
    toArray() {
        return [...this.inorderTraversal()];
    }
    
    toJSON() {
        return JSON.stringify(this._nodeToObject(this.root), null, 2);
    }
    
    _nodeToObject(node) {
        if (node === null) {
            return null;
        }
        
        return {
            data: node.data,
            left: this._nodeToObject(node.left),
            right: this._nodeToObject(node.right)
        };
    }
    
    prettyPrint(node = this.root, prefix = '', isLast = true) {
        if (this.root === null) {
            console.log('Empty tree');
            return;
        }
        
        if (node !== null) {
            console.log(prefix + (isLast ? '└── ' : '├── ') + node.data);
            
            const children = [];
            if (node.left !== null) children.push(node.left);
            if (node.right !== null) children.push(node.right);
            
            children.forEach((child, index) => {
                const isLastChild = index === children.length - 1;
                const extension = isLast ? '    ' : '│   ';
                this.prettyPrint(child, prefix + extension, isLastChild);
            });
        }
    }
    
    // Iterator Support
    
    [Symbol.iterator]() {
        return this.inorderTraversal();
    }
    
    // Conversion Methods
    
    toString() {
        return JSON.stringify([...this.inorderTraversal()]);
    }
    
    // Validation
    
    isValidBST(node = this.root, min = -Infinity, max = Infinity) {
        if (node === null) {
            return true;
        }
        
        if (node.data <= min || node.data >= max) {
            return false;
        }
        
        return this.isValidBST(node.left, min, node.data) &&
               this.isValidBST(node.right, node.data, max);
    }
    
    // Advanced Operations
    
    findLCA(data1, data2) {
        return this._findLCARecursive(this.root, data1, data2);
    }
    
    _findLCARecursive(node, data1, data2) {
        if (node === null) {
            return null;
        }
        
        if (data1 < node.data && data2 < node.data) {
            return this._findLCARecursive(node.left, data1, data2);
        } else if (data1 > node.data && data2 > node.data) {
            return this._findLCARecursive(node.right, data1, data2);
        } else {
            return node.data;
        }
    }
    
    getPathToNode(data) {
        const path = [];
        this._getPathRecursive(this.root, data, path);
        return path;
    }
    
    _getPathRecursive(node, data, path) {
        if (node === null) {
            return false;
        }
        
        path.push(node.data);
        
        if (node.data === data) {
            return true;
        }
        
        if (data < node.data && this._getPathRecursive(node.left, data, path)) {
            return true;
        }
        
        if (data > node.data && this._getPathRecursive(node.right, data, path)) {
            return true;
        }
        
        path.pop();
        return false;
    }
    
    // Static Factory Methods
    
    static fromArray(array) {
        const tree = new BinaryTree();
        array.forEach(value => tree.insert(value));
        return tree;
    }
    
    static fromSortedArray(sortedArray) {
        const tree = new BinaryTree();
        tree.root = BinaryTree._buildBalancedFromSorted(sortedArray, 0, sortedArray.length - 1);
        tree.size = sortedArray.length;
        return tree;
    }
    
    static _buildBalancedFromSorted(array, start, end) {
        if (start > end) {
            return null;
        }
        
        const mid = Math.floor((start + end) / 2);
        const node = new TreeNode(array[mid]);
        
        node.left = BinaryTree._buildBalancedFromSorted(array, start, mid - 1);
        node.right = BinaryTree._buildBalancedFromSorted(array, mid + 1, end);
        
        return node;
    }
}

// Utility Functions

function demonstrateBinaryTree() {
    console.log('🌳 Binary Tree Implementation in JavaScript');
    console.log('='.repeat(45));
    
    // Create and populate tree
    const tree = new BinaryTree();
    const values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45];
    
    console.log('\n📥 Inserting values:', values);
    values.forEach(value => tree.insert(value));
    
    console.log(`Tree size: ${tree.countNodes()}`);
    console.log(`Tree height: ${tree.height()}`);
    console.log(`Is balanced: ${tree.isBalanced()}`);
    console.log(`Is valid BST: ${tree.isValidBST()}`);
    
    // Visual representation
    console.log('\n🎨 Tree Structure:');
    tree.prettyPrint();
    
    // Traversals
    console.log('\n🚶 Tree Traversals:');
    console.log(`In-order:    [${[...tree.inorderTraversal()].join(', ')}]`);
    console.log(`Pre-order:   [${[...tree.preorderTraversal()].join(', ')}]`);
    console.log(`Post-order:  [${[...tree.postorderTraversal()].join(', ')}]`);
    console.log(`Level-order: [${[...tree.levelOrderTraversal()].join(', ')}]`);
    
    // Search operations
    console.log('\n🔍 Search Operations:');
    const searchValues = [25, 75, 50, 100];
    searchValues.forEach(value => {
        const found = tree.search(value);
        const depth = found ? tree.depth(value) : -1;
        console.log(`Search ${value}: ${found ? 'Found' : 'Not found'} (depth: ${depth})`);
    });
    
    // Level operations
    console.log('\n📏 Level Operations:');
    for (let level = 0; level <= tree.height(); level++) {
        const nodes = tree.getLevelNodes(level);
        console.log(`Level ${level}: [${nodes.join(', ')}]`);
    }
    
    // Advanced operations
    console.log('\n🔍 Advanced Operations:');
    console.log(`LCA of 25 and 35: ${tree.findLCA(25, 35)}`);
    console.log(`Path to 25: [${tree.getPathToNode(25).join(' → ')}]`);
    console.log(`Path to 80: [${tree.getPathToNode(80).join(' → ')}]`);
    
    // Statistics
    console.log(`\n📊 Tree Statistics:`);
    console.log(`Total nodes: ${tree.countNodes()}`);
    console.log(`Leaf nodes: ${tree.countLeaves()}`);
    console.log(`Height: ${tree.height()}`);
    
    // Deletion
    console.log(`\n🗑️ Deletion Operations:`);
    const deleteValues = [10, 30, 50];
    deleteValues.forEach(value => {
        console.log(`Deleting ${value}...`);
        const deleted = tree.delete(value);
        console.log(`Success: ${deleted}, New tree: ${tree}`);
        if (deleted) {
            console.log('Updated tree structure:');
            tree.prettyPrint();
        }
    });
}

function performanceTest() {
    console.log('\n⚡ Performance Testing');
    console.log('='.repeat(25));
    
    const sizes = [1000, 5000, 10000];
    
    sizes.forEach(size => {
        console.log(`\nTesting with ${size} elements:`);
        
        // Generate random data
        const data = Array.from({ length: size }, (_, i) => i);
        for (let i = data.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [data[i], data[j]] = [data[j], data[i]];
        }
        
        const tree = new BinaryTree();
        
        // Test insertion
        const insertStart = performance.now();
        data.forEach(value => tree.insert(value));
        const insertTime = performance.now() - insertStart;
        
        // Test search
        const searchData = data.slice(0, Math.min(100, data.length));
        const searchStart = performance.now();
        searchData.forEach(value => tree.search(value));
        const searchTime = performance.now() - searchStart;
        
        // Test traversal
        const traversalStart = performance.now();
        [...tree.inorderTraversal()];
        const traversalTime = performance.now() - traversalStart;
        
        console.log(`  Insertion:  ${insertTime.toFixed(2)}ms`);
        console.log(`  Search:     ${searchTime.toFixed(2)}ms`);
        console.log(`  Traversal:  ${traversalTime.toFixed(2)}ms`);
        console.log(`  Height:     ${tree.height()}`);
        console.log(`  Balanced:   ${tree.isBalanced()}`);
    });
}

function testFactoryMethods() {
    console.log('\n🏭 Factory Methods Testing');
    console.log('='.repeat(30));
    
    // Test fromArray
    const array = [3, 1, 4, 1, 5, 9, 2, 6, 5];
    const treeFromArray = BinaryTree.fromArray(array);
    console.log(`From array [${array.join(', ')}]:`);
    console.log(`Result: [${[...treeFromArray].join(', ')}]`);
    console.log(`Height: ${treeFromArray.height()}, Balanced: ${treeFromArray.isBalanced()}`);
    
    // Test fromSortedArray (creates balanced tree)
    const sortedArray = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    const balancedTree = BinaryTree.fromSortedArray(sortedArray);
    console.log(`\nFrom sorted array [${sortedArray.join(', ')}]:`);
    console.log(`Result: [${[...balancedTree].join(', ')}]`);
    console.log(`Height: ${balancedTree.height()}, Balanced: ${balancedTree.isBalanced()}`);
    
    console.log('\nBalanced tree structure:');
    balancedTree.prettyPrint();
}

// Module exports for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        TreeNode,
        BinaryTree,
        demonstrateBinaryTree,
        performanceTest,
        testFactoryMethods
    };
}

// Main execution
if (typeof window === 'undefined' && typeof global !== 'undefined') {
    // Node.js environment
    demonstrateBinaryTree();
    performanceTest();
    testFactoryMethods();
    
    console.log('\n✨ Binary Tree demonstration complete!');
}
